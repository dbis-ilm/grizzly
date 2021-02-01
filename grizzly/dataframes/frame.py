from grizzly.aggregates import AggregateType
import queue
from typing import List, Tuple
from grizzly.expression import ArithmExpr, ArithmeticOperation, BinaryExpression, BoolExpr, Constant, Expr, ColRef, FuncCall, ComputedCol, ExpressionException, ExprTraverser, LogicExpr
from grizzly.generator import GrizzlyGenerator
from grizzly.expression import ModelUDF,UDF, Param, ModelType

import inspect

from collections import namedtuple

import logging
logger = logging.getLogger(__name__)

###########################################################################
# Base DataFrame with common operations

class DataFrame(object):

  def __init__(self, columns, parents, alias: str = ""):
    super(DataFrame, self).__init__()

    if not columns:
      self.columns = []
    elif not isinstance(columns, list):
      self.columns = [columns]
    else:
      self.columns = columns

    self.computedCols = []

    if parents is None or type(parents) is list:
      self.parents = parents
    else:
      self.parents = [parents]

    self.alias = alias

  def updateRef(self, x):                                                                                               
    if isinstance(x,ColRef):                                                                                            
      x.df = self                                                                                                       
      return x                                                                                                          
    elif isinstance(x, FuncCall):                                                                                       
      for ic in x.inputCols:
        self.updateRef(ic)                                                                                                       
      return x                                                                                                          
    elif isinstance(x, str): # if only a string was given as column name                                                
      ref = ColRef(x, self)                                                                                             
      return ref   
    elif isinstance(x, BinaryExpression):
      if x.left:                                                                                           
        x.left = self.updateRef(x.left) if isinstance(x.left, Expr) else x.left                                           
      if x.right:
        x.right = self.updateRef(x.right) if isinstance(x.right, Expr) else x.right
      return x
    else:
      return x

  def hasColumn(self, colName):
    if not self.columns:
      return True

    for ref in self.columns:
      if ref.column == colName:
        return True

    return False

  def filter(self, expr):
    return Filter(expr, self)

  def project(self, cols, distinct = False):
    return Projection(cols, self, doDistinct=distinct)

  def distinct(self):
    if isinstance(self, Projection):
      self.doDistinct = True
      return self
    else:
      return Projection(None, self, doDistinct = True)

  def join(self, other, on, how="inner", comp = "="):

    if isinstance(on, list):
      
      lOn = None
      rOn = None
      from grizzly.expression import ExpressionException
      if not self.hasColumn(on[0]):
        raise ExpressionException(f"No such column {on[0]} for join in left hand side")
      else:
        lOn = ColRef(on[0], self)
      if not other.hasColumn(on[1]):
        raise ExpressionException(f"No such column {on[1]} for join in right hand side")
      else:
        rOn = ColRef(on[1], other)

      on = [lOn, rOn]

    return Join(self, other, on, how, comp)

  def groupby(self, groupCols):
    if not isinstance(groupCols, list):
      groupCols = [groupCols]
    return Grouping(groupCols, self)

  def limit(self, n: int, offset = None):
    if n < 0:
      raise ValueError(f"LIMIT must not be negative (got {n})")

    if isinstance(offset, int):
      offset = Constant(offset)


    return Limit(Constant(n), offset, self)

  def sort_values(self, by, ascending:bool=True):
    if not isinstance(by, list):
      by = [by]

    return Ordering(by,ascending, self)

  def _map(self, func, lines=[]):
    # XXX: if map is called on df it's a table UDF, if called on a projection it a scalar udf
    # df.map(myfunc) vs. df['a'].map(myfunc)

    if inspect.isfunction(func):
      if not isinstance(self, Projection):
        ValueError("functions can only be applied to projections currently")

      funcName = func.__name__

      sig = inspect.signature(func)
      fparams = sig.parameters
      params = []
      for fp in fparams:
        fptype = sig.parameters[fp].annotation.__name__
        # fptype = DataFrame._mapTypes(fptype)

        p = Param(fp,fptype)
        params.append(p)

      if lines == []:
        (lines,_) = inspect.getsourcelines(func)

      returns = sig.return_annotation.__name__
      # returns = DataFrame._mapTypes(returns)

      udf = UDF(funcName, params, lines, returns)
      call = FuncCall(funcName, self.columns, udf)

      # return self.project([call])
      return call

    elif isinstance(func, DataFrame):
      return self.join(func, on = None, how = "natural")
    else:
      print(f"error: {func} is not a function or other DataFrame")
      exit(1)

  def apply_torch_model(self, path: str, toTensorFunc, clazz, outputDict, clazzParameters: List, n_predictions: int = 1, *helperFuncs):

    if not isinstance(self, Projection):
      ValueError("classification can only be applied to a projection")
    if len(outputDict) <= 0:
      raise ValueError("output dict must not be empty")

    sqlGenerator = GrizzlyGenerator._backend.queryGenerator

    modelPathHash = abs(hash(path))
    funcName = f"grizzly_predict_{modelPathHash}"
    attrsString = "_".join([r.column for r in self.columns])

    sig = inspect.signature(toTensorFunc)
    fparams = sig.parameters
    if len(fparams) != 1:
      raise ValueError("toTensor converter must have exactly one parameter")

    toTensorInputType = sig.parameters[list(sig.parameters)[0]].annotation.__name__
    params = [Param("invalue", toTensorInputType), Param("n_predictions", "int")]
    paramsStr = ",".join([f"{p.name} {sqlGenerator._mapTypes(p.type)}" for p in params])

    # predictedType = type(outputDict[0]).__name__
    predictedType = "str"  # hard coded string because we collect n predictions in a list of strings

    helpers = list(helperFuncs)
    helperCode = "\n"
    for helperFunc in helpers:
      (funcLines, _) = inspect.getsourcelines(helperFunc)
      funcLines = sqlGenerator._unindent(funcLines)
      helperCode += "".join(funcLines)

    (encoderCode, _) = inspect.getsourcelines(toTensorFunc)
    encoderCode = sqlGenerator._unindent(encoderCode)
    encoderCode = "".join(encoderCode)

    converter = lambda x: f"\"{x}\"" if type(x) == str else f"{x}"
    outDictCode = "[" + ",".join(map(converter, outputDict)) + "]"

    modelParameters = ",".join(map(converter, clazzParameters)) if clazzParameters else ""

    (clazzCodeLst, _) = inspect.getsourcelines(clazz)
    clazzCode = "".join(clazzCodeLst)

    template_replacement_dict = {}
    template_replacement_dict["$$modelpathhash$$"] = modelPathHash
    template_replacement_dict["$$modelpath$$"] = path
    template_replacement_dict["$$encoderfuncname$$"] = toTensorFunc.__name__
    template_replacement_dict["$$helpers$$"] = helperCode
    template_replacement_dict["$$encoder$$"] = encoderCode
    template_replacement_dict["$$inputcols$$"] = paramsStr
    template_replacement_dict["$$outputdict$$"] = outDictCode
    template_replacement_dict["$$modelclassparameters$$"] = modelParameters
    template_replacement_dict["$$modelclassname$$"] = clazz.__name__
    template_replacement_dict["$$modelclassdef$$"] = clazzCode
    udf = ModelUDF(funcName, params, predictedType, ModelType.TORCH, template_replacement_dict)
    call = FuncCall(funcName, self.columns + [n_predictions] , udf, f"predicted_{attrsString}")

    # return self.project([call])
    return call

  def apply_onnx_model(self, onnx_path, input_to_tensor, tensor_to_output):
    funcName = "apply"
    attrsString = "_".join([r.column for r in self.columns])
    in_sig = inspect.signature(input_to_tensor)
    input_names = list(in_sig.parameters.keys())
    input_names_str = ','.join(input_names)
    (lines1, _) = inspect.getsourcelines(input_to_tensor)
    params = []
    for param in in_sig.parameters:
      type = in_sig.parameters[param].annotation.__name__
      if (type == "_empty"):
        raise ValueError("Input converter function must specify parameter types")
      params.append(Param(param, type))

    out_sig = inspect.signature(tensor_to_output)
    (lines2, _) = inspect.getsourcelines(tensor_to_output)
    returntype = out_sig.return_annotation.__name__
    if (returntype == "_empty"):
      raise ValueError("Output converter function must specify the return type")

    template_replacement_dict = {}
    template_replacement_dict["$$inputs$$"] = str(in_sig)
    template_replacement_dict["$$returntype$$"] = returntype
    template_replacement_dict["$$input_to_tensor_func$$"] = "".join(lines1)
    template_replacement_dict["$$tensor_to_output_func$$"] = "".join(lines2)
    template_replacement_dict["$$input_names$$"] = input_names_str
    template_replacement_dict["$$onnx_file_path$$"] = onnx_path
    template_replacement_dict["$$input_to_tensor_func_name$$"] = input_to_tensor.__name__
    template_replacement_dict["$$tensor_to_output_func_name$$"] = tensor_to_output.__name__

    udf = ModelUDF(funcName, params, returntype, ModelType.ONNX, template_replacement_dict)
    call = FuncCall(funcName, self.columns, udf, f"predicted_{attrsString}")

    # return self.project([call])
    return call

  def apply_tensorflow_model(self, tf_checkpoint_file: str, network_input_names, constants=[], vocab_file: str = ""):
    funcName = "apply"
    attrsString = "_".join([r.column for r in self.columns])

    # TODO: make this generic
    params = [Param("a", "str")]
    returntype = "int"

    template_replacement_dict = {}
    template_replacement_dict["$$tf_checkpoint_file$$"] = tf_checkpoint_file
    template_replacement_dict["$$vocab_file$$"] = vocab_file
    template_replacement_dict["$$network_input_names$$"] = f"""[{', '.join('"%s"' % n for n in network_input_names)}]"""
    template_replacement_dict["$$constants$$"] = f"[{','.join(str(item) for item in constants)}]"

    udf = ModelUDF(funcName, params, returntype, ModelType.TF, template_replacement_dict)
    call = FuncCall(funcName, self.columns, udf, f"predicted_{attrsString}")

    # return self.project([call])
    return call

  def map(self, func):
    return self._map(func)


  ###################################
  # iteration

  def __iter__(self):
    return GrizzlyGenerator.iterator(self)

  def iterrows(self):
    '''
    Iterate over DataFrame rows as (index, Array) pairs.
    '''
    num = 0
    for row in self:
      yield (num, list(row))
      num += 1


  def itertuples(self, name="Grizzly",index=None):
    '''
    Iterate over DataFrame rows as namedtuples.
    '''
    
    theIter = GrizzlyGenerator.iterator(self, includeHeader=True)

    headerRow = next(theIter)

    RowType = namedtuple(name, headerRow)

    for row in theIter:
      yield RowType._make(row)

  def items(self):
    '''
    Iterate over (column name, Array) pairs.

    Iterates over the DataFrame columns, returning a tuple with the column name and the content as a Series.
    '''
    arr = self.collect(includeHeader=True)
    header = arr[0]
    data = arr[1:]

    col = 0
    for colname in header:
      columndata = [row[col] for row in data]
      yield (colname, columndata)
      col += 1


  ###################################
  # shortcuts


  def __getattr__(self, name):
    return ColRef(name, self)


  # magic function for write access by index: []
  def __setitem__(self, key, value):
    
    if isinstance(value, Grouping):
      #get the last added agg func and set its alias name
      f = value.aggFunc[-1]
      f.alias = key
    
    elif isinstance(value, Expr) or isinstance(value, DataFrame):
      
      if isinstance(value, FuncCall):
        value.alias = key
        newCol = value
        self.updateRef(value)
      else:
        newCol = ComputedCol(value, key)

      self.computedCols.append(newCol)
    else: # not am expr or DF -> must be a constant
      newCol = ComputedCol(Constant(value), key)
      self.computedCols.append(newCol)

  # magic function for read access by index: []
  def __getitem__(self, key):
    theType = type(key)

    if isinstance(key, slice): # used for LIMIT .. OFFSET
      if key.step is not None:
        logger.warn("Step is not supported for slice access on DataFrames")

      n = key.stop

      offset = key.start if key.start is not None else None
      return self.limit(n, offset)

    elif theType is ColRef : # if in the projection list e.g. "df.a" was given
      return self.project(key)

    elif isinstance(key, BoolExpr) or isinstance(key, LogicExpr): # e.g. a filter expression
      return self.filter(key)

    elif theType is str: # a single string is given -> project to that column
      return ColRef(key,self)

    elif theType is list:
      
      projList = []
      for e in key:
        t = type(e)
        if t is str:
          projList.append(ColRef(e, self))
        elif t is ColRef:
          c = ColRef(e.colName(), self)
          projList.append(c)
        else:
          raise ExpressionException(f"expected a column name string or column reference, but got {e}")

      return self.project(projList)
    else:
      print(f"{key} has type {theType} -- ignoring")
      return self

  ###################################
  # Comparison expressions

  # @staticmethod
  # def __expressionUpdateRefs(left, right):
  #   if not isinstance(left, Projection):
  #     raise ExpressionException(f"Must have a projection to access fields, but got {type(left)}")
  #   if len(left.columns) != 1:
  #     attrsStr = ",".join([str(x) for x in left.columns]) if left.columns else ""
  #     raise ExpressionException(f"Projection list must have exactly one column, but is: {len(left.columns)}: [{attrsStr}]")

  #   if isinstance(right, Projection):
  #     r = right.columns[0]
  #     if len(right.parents) > 0:
  #       # we have a projection in an expression to reference a variable only
  #       # thus, we want to update to the original DF in order to have the correct
  #       # qualifier, instead of the one created for the projection
  #       right.parents[0].updateRef(r)
  #     else:
  #       print("a projection without a parent should not happen... is your script correct?")
  #   else:
  #     r = right

  #   # we know we are a projection. Update the projection-ref to our parent
  #   left.parents[0].updateRef(left.columns[0])

  #   return r

  # def __eq__(self, other):
  #   r = DataFrame.__expressionUpdateRefs(self, other)

  #   expr = BoolExpr(self.columns[0], r)
  #   return expr

  # def __gt__(self, other):
  #   r = DataFrame.__expressionUpdateRefs(self, other)

  #   expr = Gt(self.columns[0], r)
  #   return expr

  # def __lt__(self, other):
  #   r = DataFrame.__expressionUpdateRefs(self, other)

  #   expr = Lt(self.columns[0], r)
  #   return expr

  # def __ge__(self, other):
  #   r = DataFrame.__expressionUpdateRefs(self, other)

  #   expr = Ge(self.columns[0], r)
  #   return expr
  
  # def __le__(self, other):
  #   r = DataFrame.__expressionUpdateRefs(self, other)

  #   expr = Le(self.columns[0], r)
  #   return expr

  # def __ne__(self, other):
  #   r = DataFrame.__expressionUpdateRefs(self, other)

  #   expr = Ne(self.columns[0], r)
  #   return expr

  ###########################################################################
  # Actions
  ###########################################################################

  def info(self, verbose = None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None):
    raise NotImplementedError("This method has not been implemented yet")

  def select_types(include=None, exclude=None):
    '''
    Return a subset of the DataFrame’s columns based on the column dtypes.
    '''
    raise NotImplementedError("This method has not been implemented yet")

  def values(self):
    '''
    Return a Numpy representation of the DataFrame.
    '''
    raise NotImplementedError("This method has not been implemented yet")

  def to_numpy(self):
    '''
    Return a Numpy representation of the DataFrame.
    '''
    raise NotImplementedError("This method has not been implemented yet")

  def collect(self, includeHeader = False):
    return GrizzlyGenerator.collect(self, includeHeader)

  # Pandas DF stuff

  @property
  def shape(self):
    '''
    Return a tuple representing the dimensionality of the DataFrame.

    (number of columns, number of rows)
    '''
    f = self.project(FuncCall("count", ["*"], None, "rowcount"))
    cc = ComputedCol(f, None)
    shapeDF = self.project(['*', cc])
    shapeDF = shapeDF.limit(1)


    resultRow = GrizzlyGenerator.fetchone(shapeDF)

    numCols = len(resultRow) - 1 # -1 because of added count
    numRows = resultRow[-1] # last row would be the row count

    return (numCols, numRows)

  @property
  def at(self):
    '''
    Access a value for a row/column label pair. In contrast to Pandas this must not return
    a single value. If only row number is given, it will return that row. If a column name is given
    the entire column is returned (all rows). 
    '''
    return _Accessor(self)

  @property
  def loc(self):
    return _Accessor(self)
    
  @property  
  def iat(self):
    raise NotImplementedError("getting columns by number is not supported")

  @property
  def iloc(self):
    raise NotImplementedError("getting columns by number is not supported")

  ###################################
  # aggregation functions

  def _exec_or_add_aggr(self, f: FuncCall):
    """
    Adaption to the nested query generation. If there is a grouping in the
    operator tree, the aggregation becomes a transformation. However, it must not
    become a new nested query, but needs to be attached to the grouping.
    If there is no grouping, the aggregation is an action, so execute the query.
    """

    # if isinstance(col, Projection):
    #   assert(len(col.columns) == 1)
    #   col = self.updateRef(col.columns[0])


    # if we are a grouping  and the function is not applied on a grouping column
    # then add the aggregation to the list...
    if isinstance(self, Grouping) and len([1 for fCol in f.inputCols for groupCol in self.groupCols if fCol.column == groupCol.column]) == 0:
      self._addAggFunc(f)
      return self

    # otherwise execute f as an action
    return GrizzlyGenerator.aggregate(self, f)

  def agg(self, aggType, col, alias = None):
    if isinstance(col,str):
      col = ColRef(col, self)

    f = FuncCall(aggType, [col], None, alias)

    if isinstance(self, Grouping):
      if not col.column in [c.column for c in self.groupCols]:
        
        self._addAggFunc(f)
        return self
      else: 
        p = Projection([f], self)
        return p
    

  @staticmethod
  def _getFuncCallCol(df, col):
    '''
    guarantees to return a list of things to apply a method on
    or None if input col is None
    '''
    if col is None:
      return None
    elif isinstance(col, str):
      return [ColRef(col, df)]
    elif isinstance(col, Expr):
      return [col]
    elif isinstance(col, list):
      return col
    elif isinstance(col, DataFrame):
      return [col]
    else: 
      return [Constant(col)]


  def min(self, col=None,alias=None):
    theCol = DataFrame._getFuncCallCol(self, col)
    f = FuncCall(AggregateType.MIN, theCol, None, alias)
    return self._exec_or_add_aggr(f)

  def max(self, col=None, alias=None):
    theCol = DataFrame._getFuncCallCol(self, col)
    f = FuncCall(AggregateType.MAX, theCol, None, alias)
    return self._exec_or_add_aggr(f)

  def mean(self, col=None,alias=None):
    theCol = DataFrame._getFuncCallCol(self, col)
    f = FuncCall(AggregateType.MEAN, theCol, None, alias)
    return self._exec_or_add_aggr(f)

  def count(self, col=None, alias=None):
    theCol = DataFrame._getFuncCallCol(self, col)
    if theCol is None:
      theCol = [ColRef("*", self)]

    f = FuncCall(AggregateType.COUNT, theCol, None, alias)
    return self._exec_or_add_aggr(f)

  def sum(self , col, alias = None):
    theCol = DataFrame._getFuncCallCol(self, col)
    f = FuncCall(AggregateType.SUM, theCol, None, alias)
    return self._exec_or_add_aggr(f)


  ###################################
  # show functions

  def generate(self):
    return GrizzlyGenerator.generate(self)
  
  def generateQuery(self):
    (pre,qry) = self.generate()
    prequeries = "" if not pre else ";".join(pre)
    return f"{prequeries} {qry}"

  def show(self, pretty=False, delim=",", maxColWidth=20, limit=20):
    print(GrizzlyGenerator.toString(self,delim,pretty,maxColWidth,limit))

  def head(self,n=5):
    return self.limit(n).collect()
    # self.show(limit=n)

  def tail(self, n = 5):
    if not isinstance(self, Ordering):
      raise ValueError("can get tail only of ordered DataFrame")

    cntFunc = FuncCall(AggregateType.COUNT, [])
    prj = self.project(cntFunc)
    expr = ArithmExpr(prj, Constant(n), ArithmeticOperation.SUB)

    return self.limit(n, expr).collect()
    l.show(limit = n)
    
  # def __str__(self):
  #   strRep = GrizzlyGenerator.toString(self, pretty=True)
  #   return strRep
    # tableStr = GrizzlyGenerator.table(self)
    # return tableStr
    

  # def __repr__(self) -> str:
  #   tableStr = GrizzlyGenerator.table(self)
  #   return tableStr
    
###########################################################################
# Concrete DataFrames representing an operation


class Table(DataFrame):
  def __init__(self, table):
    self.table = table
    alias = GrizzlyGenerator._incrAndGetTupleVar()
    super().__init__([], None, alias)

class ExternalTable(DataFrame):
  def __init__(self, file, colDefs, hasHeader, delimiter, format):
    self.filenames = file
    self.colDefs = colDefs
    self.hasHeader = hasHeader
    self.delimiter = delimiter
    self.format = format
    alias = GrizzlyGenerator._incrAndGetTupleVar()
    self.table = f"temp_ext_table{alias}"
    super().__init__([], None, alias)

class Projection(DataFrame):

  def __init__(self, columns, parent: DataFrame, doDistinct = False):
   
    self.doDistinct = doDistinct
    
    if columns is None:
      columns = []
    elif not isinstance(columns, list):
      columns = [columns]

    # update references to all columns
    theCols = []
    for col in columns:
      theCol = self.updateRef(col)
      theCols.append(theCol)
      
    columns = theCols

    super().__init__(columns, parent,GrizzlyGenerator._incrAndGetTupleVar())

class Filter(DataFrame):

  def __init__(self, expr: Expr, parent: DataFrame):
    super().__init__(parent.columns, parent,GrizzlyGenerator._incrAndGetTupleVar())
    self.expr = self.updateRef(expr)

class Grouping(DataFrame):

  def __init__(self, groupCols: List, parent: DataFrame):
    self.having = []
    self.groupCols = []
    computedAliases = [c.alias for c in parent.computedCols]
    for theCol in groupCols:
      if isinstance(theCol, str):
        theRef = None
        if theCol in computedAliases:
          theRef = ColRef(theCol, None)
        else:
          theRef = ColRef(theCol, self)
        theCol = theRef
      elif isinstance(theCol, ColRef):
        self.updateRef(theCol)
      elif isinstance(theCol, Expr):
        pass
      else: 
        raise ExpressionException(f"invalid grouping column type: {type(theCol)}")

      self.groupCols.append(theCol)
    
    self.aggFunc = []

    super().__init__(self.groupCols, parent, GrizzlyGenerator._incrAndGetTupleVar())

  def _addAggFunc(self,funcCall: FuncCall):
    self.aggFunc.append(funcCall)
    

  def filter(self, expr):
    # the expression might contain references to computed columns
    # update the refs so that these column references are not prefixed

    aggColNames = [x.alias for x in self.aggFunc]

    cols = []

    def visitor(e):
      if isinstance(e, ColRef):
        cols.append(e)
        
    ExprTraverser.df(expr, visitor)

    isHaving = False
    for c in cols:
      if c.column in aggColNames: # if the referenced column is computed using an aggregate we must add the expression to having
        isHaving = True
        c.df = None

    if isHaving:
      self.having.append(expr)
      return self
    
    
    return super().filter(expr)

class Join(DataFrame):
  def __init__(self, parent, other, on, how, comp):
    t = GrizzlyGenerator._incrAndGetTupleVar()
    super().__init__(parent.columns + other.columns, parent, t)
    self.right = other
    self.on = on
    self.how = how
    self.comp = comp

  def leftParent(self):
    return self.parents[0]

  def rightParent(self):
    return self.right

class Limit(DataFrame):
  def __init__(self, limit: int, offset: int, parent):
    super().__init__(parent.columns, parent, GrizzlyGenerator._incrAndGetTupleVar())
    self.limit = limit
    self.offset = offset

class Ordering(DataFrame):
  def __init__(self, by:list, ascending:bool, parent):
    super().__init__(parent.columns, parent, GrizzlyGenerator._incrAndGetTupleVar())
    
    sortCols = []
    for col in by:
      if isinstance(col, Projection):
        sortCols.append(self.updateRef(col.columns[0]))
      elif isinstance(col, str):
        sortCols.append(ColRef(col, self))
      elif isinstance(col, ColRef):
        sortCols.append(self.updateRef(col))
      else:
        raise ExpressionException(f"unsupported type for oder by value: {type(col)}")

    self.by = sortCols
    self.ascending = ascending


#########################
# helpers

class _Accessor:

  def __init__(self, df):
    self.df = df
    super().__init__()

  def __getitem__(self, loc):

    row = None
    col = None

    if isinstance(loc, int): # a row number: OFFSET loc LIMIT 1 
      row = loc
    elif isinstance(loc, str): # a column name: Projection
      col = loc
    elif isinstance(loc, ColRef):
      col = loc.column
    elif isinstance(loc, Tuple): # row + column
      if len(loc) != 2:
        raise ValueError(f"Invalid length of access tuple: {len(loc)}, required: 2")

      row = loc[0]
      col = loc[1]
    else:
      raise ValueError(f"invalid parameter values to at! type: {type(loc)}")

    result = self.df
    
    if col:
      result = result.project([col])
    
    if row:
      result = result.limit(n=1, offset=row)

    return result.collect()

class Traverser:
  
  @staticmethod
  def bf(df: DataFrame, visitorFunc):
    todo = queue.Queue()
    todo.put_nowait(df)

    while todo.qsize() > 0:
      current = todo.get_nowait()

      for parent in current.parents:
        todo.put_nowait(parent)

      
      visitorFunc(current)

  @staticmethod
  def df(df: DataFrame, visitorFunc):
    todo = queue.LifoQueue()
    todo.put_nowait(df)

    while todo.qsize() > 0:
      current = todo.get_nowait()

      for parent in current.parents:
        todo.put_nowait(parent)
      
      visitorFunc(current)    

