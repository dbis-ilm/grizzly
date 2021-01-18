from grizzly.expression import ComputedCol, Eq, Ne, Ge, Gt, Le, Lt, Expr, ColRef, ComputedCol, FuncCall, ExpressionException
from grizzly.generator import GrizzlyGenerator
from grizzly.aggregates import AggregateType
from grizzly.expression import ModelUDF,UDF, Param, ModelType

import inspect

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
      x.df = self
      for ic in x.inputCols:
        self.updateRef(ic)                                                                                                       
      return x                                                                                                          
    elif isinstance(x, str): # if only a string was given as column name                                                
      ref = ColRef(x, self)                                                                                             
      return ref                                                                                                        
    elif isinstance(x, Expr):
      if x.left:                                                                                           
        x.left = self.updateRef(x.left) if isinstance(x.left, Expr) else x.left                                           
      if x.right:
        x.right = self.updateRef(x.right) if isinstance(x.right, Expr) else x.right
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

  def project(self, cols):
    if not isinstance(cols, list):
      cols = [cols]

    return Projection(cols, self)

  def distinct(self):
    if isinstance(self, Projection):
      self.doDistinct = True
      return self
    else:
      return Projection(None, self, doDistinct = True)

  def join(self, other, on, how="inner", comp = "="):

    if isinstance(on, list):
      
      from grizzly.expression import ExpressionException
      if not self.hasColumn(on[0]):
        raise ExpressionException(f"No such column {on[0]} for join in left hand side")
      if not other.hasColumn(on[1]):
        raise ExpressionException(f"No such column {on[1]} for join in right hand side")

    return Join(self, other, on, how, comp)

  def groupby(self, groupCols):
    if not isinstance(groupCols, list):
      groupCols = [groupCols]
    return Grouping(groupCols, self)

  def limit(self, n: int, offset: int = -1):
    if n < 0:
      raise ValueError(f"LIMIT must not be negative (got {n})")

    return Limit(n, offset, self)

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
      call = FuncCall(funcName, self.columns, self, udf)

      return self.project([call])

    elif isinstance(func, DataFrame):
      return self.join(func, on = None, how = "natural")
    else:
      print(f"error: {func} is not a function or other DataFrame")
      exit(1)

  def apply_torch_model(self, path: str, toTensorFunc, clazz, outputDict, clazzParameters: list, n_predictions: int = 1, *helperFuncs):

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
    call = FuncCall(funcName, self.columns + [n_predictions] , self,udf, f"predicted_{attrsString}")

    return self.project([call])

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
    call = FuncCall(funcName, self.columns, self, udf, f"predicted_{attrsString}")

    return self.project([call])

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
    call = FuncCall(funcName, self.columns, self, udf, f"predicted_{attrsString}")

    return self.project([call])

  def map(self, func):
    return self._map(func)

  ###################################
  # shortcuts

  def __getattr__(self, name):
    # if isinstance(self, Projection) or isinstance(self, Grouping):
    #   return ColRef(name, self)
    # else:
    return Projection([ColRef(name, self)],self)

  # magic function for write access by index: []
  def __setitem__(self, key, value):
    if isinstance(value, Projection):
      value.columns[0].alias = key
      newCol = value.parents[0].parents[0].updateRef(value.columns[0])
      self.computedCols += [newCol]
    elif isinstance(value, Grouping):
      #get the last added agg func and set its alias name
      (lastFuncType, lastFuncCol, _) = value.aggFunc[len(value.aggFunc)-1]
      d = (lastFuncType, lastFuncCol, key)
      value.aggFunc = value.aggFunc[:-1]
      value.aggFunc.append(d)
    else:
      newCol = ColRef(value, self, key)
      self.computedCols += [newCol]
    # self.computedCols.append(ComputedCol(key,value))

  # magic function for read access by index: []
  def __getitem__(self, key):
    theType = type(key)

    if isinstance(key, slice): # used for LIMIT .. OFFSET
      if key.step is not None:
        logger.warn("Step is not supported for slice access on DataFrames")

      n = key.stop

      offset = key.start if key.start is not None else -1
      return self.limit(n, offset)

    if isinstance(key, Expr): # e.g. a filter expression
      # print(f"filter col: {key}")
      return self.filter(key)
    elif theType is str: # a single string is given -> project to that column
      return self.project(ColRef(key,None))
      # c = 
      # return Projection([ColRef(key, self)],self)
    elif theType is Projection: # if in the projection list e.g. "df.a" was given
      return self.project([key.columns[0]])
    elif theType is list:
      
      projList = []
      for e in key:
        t = type(e)
        if t is str:
          projList.append(ColRef(e, self))
        elif t is Projection:
          assert(len(e.columns) == 1)
          c = e.columns[0]
          projList.append(c)
        elif t is ColRef:
          c = ColRef(e.colName(), self)
          projList.append(c)
        else:
          raise ExpressionException(f"expected a column name string or projection, but got {e}")

      return self.project(projList)
    else:
      print(f"{key} has type {theType} -- ignoring")
      return self

  ###################################
  # Comparison expressions

  @staticmethod
  def __expressionUpdateRefs(left, right):
    if not isinstance(left, Projection):
      raise ExpressionException(f"Must have a projection to access fields, but got {type(self)}")
    if len(left.columns) != 1:
      attrsStr = ",".join([str(x) for x in self.columns]) if self.columns else ""
      raise ExpressionException(f"Projection list must have exactly one column, but is: {len(self.columns)}: [{attrsStr}]")

    if isinstance(right, Projection):
      r = right.columns[0]
      if len(right.parents) > 0:
        # we have a projection in an expression to reference a variable only
        # thus, we want to update to the original DF in order to have the correct
        # qualifier, instead of the one created for the projection
        right.parents[0].updateRef(r)
      else:
        print("a projection without a parent should not happen... is your script correct?")
    else:
      r = right

    # we know we are a projection. Update the projection-ref to our parent
    left.parents[0].updateRef(left.columns[0])

    return r

  def __eq__(self, other):
    r = DataFrame.__expressionUpdateRefs(self, other)

    expr = Eq(self.columns[0], r)
    return expr

  def __gt__(self, other):
    r = DataFrame.__expressionUpdateRefs(self, other)

    expr = Gt(self.columns[0], r)
    return expr

  def __lt__(self, other):
    r = DataFrame.__expressionUpdateRefs(self, other)

    expr = Lt(self.columns[0], r)
    return expr

  def __ge__(self, other):
    r = DataFrame.__expressionUpdateRefs(self, other)

    expr = Ge(self.columns[0], r)
    return expr
  
  def __le__(self, other):
    r = DataFrame.__expressionUpdateRefs(self, other)

    expr = Le(self.columns[0], r)
    return expr

  def __ne__(self, other):
    r = DataFrame.__expressionUpdateRefs(self, other)

    expr = Ne(self.columns[0], r)
    return expr

  ###########################################################################
  # Actions
  ###########################################################################

  def collect(self, includeHeader = False):
    return GrizzlyGenerator.collect(self, includeHeader)

  ###################################
  # aggregation functions

  def _exec_or_add_aggr(self, col, aggFunc, alias: str):
    """
    Adaption to the nested query generation. If there is a grouping in the
    operator tree, the aggregation becomes a transformation. However, it must not
    become a new nested query, but needs to be attached to the grouping.
    If there is no grouping, the aggregation is an action, so execute the query.
    """

    if isinstance(col, Projection):
      assert(len(col.columns) == 1)
      col = self.updateRef(col.columns[0])

    if isinstance(self, Grouping) and aggFunc and not col.column in [c.column for c in self.groupCols]:
      self._addAggFunc(aggFunc, col, alias)
      return self

    return GrizzlyGenerator.aggregate(self, col, aggFunc,alias)

  def agg(self, aggType, col, alias = None):
    # self.aggFunc.append((aggType, col, alias))
    if isinstance(col,str):
      col = ColRef(col, self)

    if isinstance(self, Grouping):
      if not col.column in [c.column for c in self.groupCols]:
        self._addAggFunc(aggType, col, alias)
        return self
      else: 
        func = FuncCall(aggType,[col],self,None,alias)
        p = Projection([func], self)
        return p
    


  def min(self, col=None,alias=None):
    # return self._execAgg("min",col)
    return self._exec_or_add_aggr(col, AggregateType.MIN, alias)

  def max(self, col=None, alias=None):
    # return self._execAgg("max",col)
    return self._exec_or_add_aggr(col, AggregateType.MAX, alias)

  def mean(self, col=None,alias=None):
    # return self._execAgg('avg',col)
    return self._exec_or_add_aggr(col, AggregateType.MEAN, alias)

  def count(self, col=None, alias=None):
    colName = "*"
    if col is not None:
      colName = ColRef(col,self)
    
    return self._exec_or_add_aggr(colName, AggregateType.COUNT,alias)

  def sum(self , col, alias = None):
    # return GrizzlyGenerator.aggregate(self, col, AggregateType.SUM)
    return self._exec_or_add_aggr(col, AggregateType.SUM, alias)
    # return self._execAgg("sum", col)


  def _hasGrouping(self):
    curr = self
    while curr is not None:
      if isinstance(curr, Grouping):
        return curr

      # FIXME: how to handle join paths?
      if curr.parents is not None:
        curr = curr.parents[0]
      else:
        curr = None

    return None

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
    
  def __str__(self):
    strRep = GrizzlyGenerator.toString(self, pretty=True)
    return strRep
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

  def __init__(self, columns:list[ColRef], parent: DataFrame, doDistinct = False):
   
    self.doDistinct = doDistinct
    
    if columns and parent:
      columns = [self.updateRef(x) for x in columns] if not isinstance(columns,str) else [ColRef(columns, self)]
    else:
      columns = []

    super().__init__(columns, parent,GrizzlyGenerator._incrAndGetTupleVar())

class Filter(DataFrame):

  def __init__(self, expr: Expr, parent: DataFrame):
    super().__init__(parent.columns, parent,GrizzlyGenerator._incrAndGetTupleVar())
    self.expr = self.updateRef(expr)

class Grouping(DataFrame):

  def __init__(self, groupCols, parent):
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
        self.groupCols.append(theRef)
      else:
        theCol.df = self
        self.groupCols.append(theCol)
    
    self.aggFunc = []

    super().__init__(self.groupCols, parent, GrizzlyGenerator._incrAndGetTupleVar())

  def _addAggFunc(self,func, col, alias):
    self.aggFunc.append((func,col, alias))
    

  def filter(self, expr):
    
    # TODO: traverse expression tree and collect all ColRefs and FuncCalls 
    # update them. 
    if expr.left.column in [x[2] for x in self.aggFunc]:
      # unset df reference, since this is actually a computed column
      # otherwise the generator would qualify this with e.g. _t1.
      # however, the aggregate does not belong to _t1, yet, but rather is 
      # being computed
      expr.left.df = None 
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
