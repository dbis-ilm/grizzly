from grizzly.dataframes.schema import ColType, Schema, SchemaError
from grizzly.aggregates import AggregateType
import queue
from typing import List, Tuple, Callable
from grizzly.expression import AllColumns, ArithmExpr, ArithmeticOperation, BinaryExpression, BoolExpr, Constant, Expr, ColRef, FuncCall, ComputedCol, ExpressionException, ExprTraverser, LogicExpr, BooleanOperation, SetExpr, SetOperation
from grizzly.generator import GrizzlyGenerator
from grizzly.expression import ModelUDF,UDF, Param, ModelType
from grizzly.udfcompiler.udfcompiler_exceptions import UDFCompilerException


import inspect

from collections import namedtuple

import logging
logger = logging.getLogger(__name__)


class GrizzlyIndexError(Exception):
  def __init__(self, *args: object) -> None:
      super().__init__(*args)

###########################################################################
# Base DataFrame with common operations

class DataFrame(object):

  def __init__(self, schema, parents, alias: str = "", index=None):
    super(DataFrame, self).__init__()

    self.index = index

    if isinstance(schema, dict):
      schema = Schema(dict)
    elif schema is None:
      schema = Schema(schema)

    self._schema = schema
    self.computedCols = []

    if parents is None or type(parents) is list:
      self.parents = parents
    else:
      self.parents = [parents]

    self.alias = alias

  @property
  def schema(self):
    return self._schema

  def _updateRef(self, x):                                                                                               
    if isinstance(x,ColRef):                                                                                            
      x.df = self                                                                                                       
      return x                                                                                                          
    elif isinstance(x, FuncCall):                                                                                       
      for ic in x.inputCols:
        self._updateRef(ic)                                                                                                       
      return x                                                                                                          
    elif isinstance(x, str): # if only a string was given as column name                                                
      ref = ColRef(x, self)                                                                                             
      return ref   
    elif isinstance(x, BinaryExpression):
      if x.left: #and isinstance(x.left, Expr):
          x.left = self._updateRef(x.left) 

      if x.right: # and isinstance(x.right, Expr):
          x.right = self._updateRef(x.right)

      return x
    elif isinstance(x, list) or isinstance(x, tuple):
      return [self._updateRef(y) for y in x]
    else:
      return x

  def _hasColumn(self, colName):

    if isinstance(colName, ColRef):
      colName = colName.colName()

    if len(self.schema) <= 0 or colName is None or len(colName.strip()) == 0:
      return True


    hasCol = colName.lower() in self.schema
    return hasCol

  def filter(self, expr):
    return Filter(expr, self)

  def project(self, cols, distinct = False):
    return Projection(cols, self, doDistinct=distinct)

  def distinct(self):
    return Projection(None, self, doDistinct = True)

  def join(self, other, on, how="inner", comp = "="):

    if isinstance(on, list):
      
      lOn = None
      rOn = None
      from grizzly.expression import ExpressionException
      if not self._hasColumn(on[0]):
        raise ExpressionException(f"No such column {on[0]} for join in left hand side")
      else:
        lOn = ColRef(on[0], self)
      if not other._hasColumn(on[1]):
        raise ExpressionException(f"No such column {on[1]} for join in right hand side. Has cols: {other.schema}")
      else:
        rOn = ColRef(on[1], other)

      on = [lOn, rOn]

    return Join(self, other, on, how, comp)

  def union(self, other, distinct = False, by = None):
    left = self
    right = other
    if by is not None:
      if not isinstance(by, list):
        raise ValueError(f"by clause for union must be a list of columns, but got {by}")

      left = self.project(by)
      right = other.project(by)

    return Union(left, right, distinct)

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

  def sort_values(self, by, ascending=None):
    if not isinstance(by, list):
      by = [by]
   
    if ascending and isinstance(ascending, list) and not len(ascending) == len(by):
      raise ValueError(f"List of columns and list of orders must be equal")
    return Ordering(by, ascending, self)

  def map(self, func, lang='py', fallback=False):
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

        p = Param(fp,fptype)
        params.append(p)

      # if lines == []:
      (lines,_) = inspect.getsourcelines(func)

      returns = sig.return_annotation.__name__

      udf = UDF(funcName, params, lines, returns, lang, func, fallback)
      call = FuncCall(funcName, self.columns, udf)

      # return self.project([call])
      return call

    elif isinstance(func, DataFrame):
      return self.join(func, on = None, how = "natural")
    else:
      raise ValueError(f"{func} is not a function or other DataFrame")


  ###################################
  # iteration

  def __contains__(self, item):
    '''
    Implementation of 'in' operator: check if a value/tuple exists in the dataframe

    :param item: value to check If it is a tuple, it is checked if it exists in the dataframe. 
                                If it is a single string, it is checked if it is a column name.
    :return: True if the value exists in the dataframe, False otherwise

    '''

    if not self.schema:
      raise SchemaError("Cannot check if tuple exists in dataframe without schema")

    if not isinstance(item, tuple) and not isinstance(item, list):
      item = [item]

    if len(item) != len(self.schema):
      raise ValueError(f"Tuple must have same length as schema: tuple has {len(item)} columns, schema has {len(self.schema)} columns")


    constants = [Constant(x) for x in item]
    cols = self.schema.columns(df = self)

    for(c,x) in zip(cols, constants):
      if not self.schema.checkType(c,x):
        raise TypeError(f"Type mismatch: type of column {c} does not match type of value {x} ({type(x)})")

    expr = BoolExpr(cols,  constants, BooleanOperation.EQ)
    
    f = self.filter(expr)

    i = GrizzlyGenerator.iterator(f, includeHeader=False)

    try:
      i.__next__()
      return True
    except StopIteration:
      return False

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
        self._updateRef(value)
      else:
        newCol = ComputedCol(value, key)

      self.computedCols.append(newCol)
      self.schema.append(newCol)
    else: # not am expr or DF -> must be a constant
      newCol = ComputedCol(Constant(value), key)
      self.schema.append(newCol)
      self.computedCols.append(newCol)

  # magic function for read access by index: []
  def __getitem__(self, key):
    theType = type(key)

    if isinstance(key, slice): # used for LIMIT .. OFFSET
      if key.step is not None:
        logger.warn("Step is not supported for slice access on DataFrames")

      n = key.stop

      offset = key.start # if key.start is not None else None
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

  def describe(self):
    # min, max, (avg), count, count distinct

    unioned = None
    for col in self.schema.columns(lambda t : t[1] == ColType.NUMERIC):
      ref = ColRef(col, self)
      fMin = FuncCall(AggregateType.MIN, [ref],alias = "min")
      fMax = FuncCall(AggregateType.MAX, [ref],alias = "max")
      fAvg = FuncCall(AggregateType.MEAN, [ref],alias = "mean")
      fCount = FuncCall(AggregateType.COUNT, [ref], alias ="count")

      p = self.project([fMin, fMax, fAvg, fCount])
      if unioned is None:
        unioned = p
      else:
        unioned = unioned.union(p)

    return unioned


  def __len__(self) -> int:
    f = FuncCall(AggregateType.COUNT, [AllColumns(self)],None, "rowcount")
    cnter = self.project([f])

    # res is a tuple! We are only interested in the first element
    res = GrizzlyGenerator.fetchone(cnter)[0]
    return res

  @property
  def shape(self):
    '''
    Return a tuple representing the dimensionality of the DataFrame.

    (number of columns, number of rows)
    '''
    f = self.project(FuncCall("count", [AllColumns(self)], None, "rowcount"))
    cc = ComputedCol(f)

    allCols = AllColumns(self)

    shapeDF = self.project([allCols, cc])
    shapeDF = shapeDF.limit(1)


    resultRow = GrizzlyGenerator.fetchone(shapeDF)

    numCols = len(resultRow) - 1 # -1 because of added count
    numRows = resultRow[-1] # last row would be the row count

    return (numCols, numRows)

  @property
  def at(self):
    '''
    Access a value for a row/column label pair. 
    
    One element: column name; Tuple: [index_value, column_name]
    '''

    if not self.index:
      raise GrizzlyIndexError("No index column set!")

    return _IndexAccessor(self)

  @property
  def loc(self):
    return _IndexLocator(self)
    
  @property  
  def iat(self):
    raise NotImplementedError("getting columns by number is not supported")

  @property
  def iloc(self):
    raise NotImplementedError("getting columns by number is not supported")

  ###################################
  # aggregation functions

  # TODO: the aggregates on a Pandas DF return the corresponding aggregated value _per column_!
  # i.e. on a DF { a, b, c} : df.count() returns count(a), count(b), count(c)

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

    theCol = DataFrame._getFuncCallCol(self, col)

    f = FuncCall(aggType, theCol, None, alias)
    
    # the aggregate is to be called on either the grouping column (if there is a grouping)
    # or on any other column. Thus, check if this column is present in the schema.
    if not self._hasColumn(theCol[0]):
      raise SchemaError("No such column: "+str(theCol[0]))

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
    return self.__genTableAgg(col, AggregateType.MIN, lambda c: c[1] == ColType.NUMERIC or c[1] == ColType.TEXT or c[1] == ColType.UNKNOWN)

  def max(self, col=None, alias=None):
    return self.__genTableAgg(col, AggregateType.MAX, lambda c: c[1] == ColType.NUMERIC or c[1] == ColType.TEXT or c[1] == ColType.UNKNOWN)

  def mean(self, col=None,alias=None):
    # MEAN only over numeric columns
    return self.__genTableAgg(col, AggregateType.MEAN, lambda c: c[1] == ColType.NUMERIC or c[1] == ColType.UNKNOWN)

  def count(self, col=None, alias=None):
    return self.__genTableAgg(col, AggregateType.COUNT, lambda _: True)

  def sum(self , col=None, alias = None):
    # SUM only over numeric columns
    return self.__genTableAgg(col, AggregateType.SUM, lambda c: c[1] == ColType.NUMERIC or c[1] == ColType.UNKNOWN)

  def __genTableAgg(self, col, aggType, filterFunc):
    if not self.schema and col is None:
      raise SchemaError("must have a schema to compute aggregations over table")


    if col is None:
      col = self.schema.columns(filterFunc)
    elif not isinstance(col, list):
      col = [col]

    aggName = AggregateType.getName(aggType)

    result = None
    for colName in col:
      theCols = DataFrame._getFuncCallCol(self, colName)
      theCol = theCols[0]
      self.schema.check(theCol)

      colType = self.schema[theCol.colName()]
      if not filterFunc(("",colType)):
        raise SchemaError(f"cannot apply function {aggName} to column of type {colType} (column: {theCol.colName()})")

      f = FuncCall(aggType, theCols, alias=aggName)
      proj = [Constant(theCol.column, "colname"), f]
      if result is None:
        result = self.project(proj)
      else:
        prj = self.project(proj)
        result = result.union(prj)

    if len(col) == 1:
      # fetch single value. Consists of two columns (col name and value) -> return only the value
      t = result.first()
      if t is not None:
        result = t[1]

    return result
 

  ###################################
  # show functions

  def generate(self):
    return GrizzlyGenerator.generate(self)
  
  def generateQuery(self):
    (pre,qry) = self.generate()
    prequeries = "" if not pre else ";".join(pre)
    return f"{prequeries} {qry}"

  def show(self, pretty=False, delim=",", maxColWidth=20, limit=20):
    try:
      print(GrizzlyGenerator.toString(self,delim,pretty,maxColWidth,limit))
    except UDFCompilerException:
      print(self._fallback())

  def _fallback(self):
    funccall_found = False
    table = self

    # Find first funccall and remove computedCols from DataFrame
    while not funccall_found:
      # TODO: handle multiple funccalls in Fallback
      for x in table.computedCols:
        if isinstance(x, FuncCall):
          funccall = x
          table.computedCols.remove(funccall)
          funccall_found = True
      # Get parent df if current df has no funccall objekt in computedCols 
      table = table.parents[0]

    if funccall.udf.fallback == False:
      raise
    else:
      # Fallback to apply udf local with pandas
      logger.info('Fallback to UDF execution with pandas')
      # Get Parameters for UDF
      inputcols = ", ".join(str(col.column).upper() for col in funccall.inputCols)

      # Download Data into DataFrame (SQL statement without projection of UDF)
      p_df = GrizzlyGenerator.to_df(table)

      # Different handlings for single and multiple parameters
      if len(funccall.inputCols) == 1:
        p_df[funccall.alias] = p_df[inputcols].apply(funccall.udf.func)
      else:
        raise NotImplementedError('Fallback for UDFs with more than one parameter not supported yet')
        #params = []
        #for p in funccall.inputCols:
        #  params.append(p_df[str(p.column).upper()])
        #import numpy
        #vfunc = numpy.vectorize(funccall.udf.func)
        #p_df[funccall.alias] = vfunc(params)
      return p_df

  def first(self):
    tup = GrizzlyGenerator.fetchone(self)
    if len(tup) >= 1:
      return tup
    # elif len(tup) == 1:
    #   return tup
    else:
      return None


  def head(self,n=5):
    return self.limit(n).collect()
    # self.show(limit=n)

  def tail(self, n = 5):
    if not isinstance(self, Ordering):
      raise ValueError("can get tail only of ordered DataFrame")


    # add a count 
    cntFunc = FuncCall(AggregateType.COUNT, inputCols=[])
    prj = self.project(cntFunc)

    # add the offset: count - n
    expr = ArithmExpr(prj, Constant(n), ArithmeticOperation.SUB)

    return self.limit(n=n, offset=expr).collect()
    
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
  def __init__(self, table, index, schema):
    self.table = table
    alias = GrizzlyGenerator._incrAndGetTupleVar()

    if index is not None and not (isinstance(index, str) or isinstance(index, list)):
      raise ValueError(f"index definition must be a string or list of strings, but is {type(index)}")

    super().__init__(schema, None, alias, index)

class ExternalTable(DataFrame):
  def __init__(self, file, schema, hasHeader, delimiter, format, fdw_extension_name):
    self.filenames = file
    self.colDefs = schema
    self.hasHeader = hasHeader
    self.delimiter = delimiter
    self.format = format
    self.fdw_extension_name = fdw_extension_name
    alias = GrizzlyGenerator._incrAndGetTupleVar()
    self.table = f"temp_ext_table{alias}"

    theSchema = Schema.fromList(schema)
    super().__init__(theSchema, None, alias)

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
      if not isinstance(col, AllColumns):

        parent.schema.check(col)

        theCol = self._updateRef(col)
      else:
        theCol = col
      theCols.append(theCol)
      
    self.columns = theCols

    newSchema = parent.schema.infer(self.columns)

    super().__init__(newSchema, parent,GrizzlyGenerator._incrAndGetTupleVar())

  def agg(self, aggType, col, alias = None):

    # if we have only aggregate functions, just add this one to the projection list
    nonFuncs = list(filter(lambda c: not isinstance(c, FuncCall), self.columns))
    if len(nonFuncs) > 0:
      # we have non-FuncCall columns -> not everything is an aggregate function
      # thus, we need a new projection
      return super().agg(aggType, col, alias)


    theCol = DataFrame._getFuncCallCol(self, col)
    f = FuncCall(aggType, theCol, None, alias)

    # add the new FuncCall to the list and adapt Schema
    self._addToList(f)

    return self

  def _addToList(self, col):
    c = self._updateRef(col)
    self.columns.append(c)
    self.schema.append(c)

  def distinct(self):
    self.doDistinct = True
    return self

  def apply_torch_model(self, path: str, toTensorFunc, clazz, outputDict, clazzParameters: List, n_predictions: int = 1, *helperFuncs):

    if len(outputDict) <= 0:
      raise ValueError("output dict must not be empty")

    # TODO maybe better to create a new UDF object and pass it to the code generator
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


class Filter(DataFrame):

  def __init__(self, expr: Expr, parent: DataFrame):

    parent.schema.check(expr)
    self.expr = self._updateRef(expr)
    super().__init__(parent.schema, parent,GrizzlyGenerator._incrAndGetTupleVar())

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
        self._updateRef(theCol)
      elif isinstance(theCol, Expr):
        pass
      else: 
        raise ExpressionException(f"invalid grouping column type: {type(theCol)}")

      parent.schema.check(theCol)

      self.groupCols.append(theCol)
    
    self.aggFunc = []
    
    newSchema = parent.schema.infer(self.groupCols)
    super().__init__(newSchema, parent, GrizzlyGenerator._incrAndGetTupleVar())

  def agg(self, aggType, col, alias = None):
    # if this is called on a grouping, add the aggregation function - 
    # BUT only if it is not called on a grouping column
    # 
    # if the aggregation is called on a grouping column, then add a new projection
    #
    # if it is not a Grouping, then also add a new projection 
    theCol = DataFrame._getFuncCallCol(self, col)
    f = FuncCall(aggType, theCol, None, alias)

    if not theCol[0].column in [c.column for c in self.groupCols]:
      self._addAggFunc(f)
      return self

    return super().agg(aggType, col, alias)

  def _addAggFunc(self,funcCall: FuncCall):
    self.aggFunc.append(funcCall)
    self.schema.append(funcCall)
    

  def filter(self, expr):
    # the expression might contain references to computed columns
    # update the refs so that these column references are not prefixed

    self.schema.check(expr)

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

  def sum(self, col, alias = None):
    if col is None:
        raise ValueError("must specify a column to aggregate!")

    theCol = DataFrame._getFuncCallCol(self, col)
    f = FuncCall(AggregateType.SUM, theCol, None, alias)
    return self._exec_or_add_aggr(f)

  def count(self, col = None, alias = None):
    theCol = DataFrame._getFuncCallCol(self, col)
    if theCol is None:
      theCol = [AllColumns(self)]

    f = FuncCall(AggregateType.COUNT, theCol, None, alias)
    return self._exec_or_add_aggr(f)

  def min(self, col, alias = None):
    if col is None:
        raise ValueError("must specify a column to aggregate!")

    theCol = DataFrame._getFuncCallCol(self, col)
    f = FuncCall(AggregateType.MIN, theCol, None, alias)
    return self._exec_or_add_aggr(f)

  def max(self, col, alias = None):
    if col is None:
      raise ValueError("must specify a column to aggregate!")

    theCol = DataFrame._getFuncCallCol(self, col)
    f = FuncCall(AggregateType.MAX, theCol, None, alias)
    return self._exec_or_add_aggr(f)

  def mean(self, col, alias = None):
    if col is None:
      raise ValueError("must specify a column to aggregate!")

    theCol = DataFrame._getFuncCallCol(self, col)
    f = FuncCall(AggregateType.MEAN, theCol, None, alias)
    return self._exec_or_add_aggr(f)

class Join(DataFrame):
  def __init__(self, parent, other, on, how, comp):
    t = GrizzlyGenerator._incrAndGetTupleVar()
    self.right = other
    self.on = on
    self.how = how
    self.comp = comp

    resultSchema = parent.schema.merge(other.schema)
    if isinstance(on, Expr):
      resultSchema.check(on)
    # self.columns = parent.columns + other.columns

    super().__init__(resultSchema, parent, t)

  def leftParent(self):
    return self.parents[0]

  def rightParent(self):
    return self.right

class Union(DataFrame):
  def __init__(self, parent, other, distinct):
    # TODO check schemas match!
    
    self.other = other
    self.distinct = distinct

    super().__init__(parent.schema, parent)

  def leftParent(self):
    return self.parents[0]

  def rightParent(self):
    return self.other

class Limit(DataFrame):
  def __init__(self, limit, offset, parent):
    self.limit = limit
    self.offset = offset
    super().__init__(parent.schema, parent, GrizzlyGenerator._incrAndGetTupleVar())

class Ordering(DataFrame):
  def __init__(self, by:list, ascending, parent):
    super().__init__(parent.schema, parent, GrizzlyGenerator._incrAndGetTupleVar())
    
    sortCols = []
    for col in by:
      if isinstance(col, Projection):
        sortCols.append(self._updateRef(col.columns[0]))
      elif isinstance(col, str):
        sortCols.append(ColRef(col, self))
      elif isinstance(col, ColRef):
        sortCols.append(self._updateRef(col))
      else:
        raise ExpressionException(f"unsupported type for oder by value: {type(col)}")

    parent.schema.check(sortCols)

    self.by = sortCols
    self.ascending = ascending


#########################
# helpers

class _IndexAccessor:
  def __init__(self, df):
    self.df = df
    super(_IndexAccessor, self).__init__()

  def __getitem__(self, at):
    # TODO: handle assigning to the specified position

    indexCol = ColRef(self.df.index, self.df)
    if isinstance(at, Tuple):
      row = at[0]
      col = at[1]
      expr = BoolExpr(indexCol, Constant(row), BooleanOperation.EQ)
      return self.df.filter(expr).project(col).first()
    elif isinstance(at, str) or isinstance(at, ColRef):
      # we expect the accessor to be a column name
      return self.df.project(at).first()
    else:
      raise ValueError(f"invalid argument to at. Expected column name or tuple, but got {type(at)}")

class _IndexLocator:
  def __init__(self, df):
    self.df = df
    super(_IndexLocator, self).__init__()

  def __getitem__(self, loc):
    indexCol = ColRef(self.df.index, self.df)
    if isinstance(loc, list):
      # TODO: handle passing boolean array as mask
      expr = SetExpr(indexCol, loc, SetOperation.IN)
      return self.df.filter(expr)
    elif isinstance(loc, Tuple):
      row = loc[0]
      col = loc[1]
      expr = BoolExpr(indexCol, Constant(row), BooleanOperation.EQ)
      return self.df.filter(expr).project(col)
    elif isinstance(loc, slice):
      start = loc.start
      stop = loc.stop

      return self.df[ (indexCol >= start) & (indexCol <= stop) ]

    elif isinstance(loc, Callable):
      raise NotImplementedError("passing callable is not supported yet")
    else: # treat as a single row label 
      expr = BoolExpr(indexCol, Constant(loc), BooleanOperation.EQ)
      return self.df.filter(expr)
    

# class _Accessor:

#   def __init__(self, df):
#     self.df = df
#     super().__init__()

#   def __getitem__(self, loc):

#     row = None
#     col = None

#     if isinstance(loc, int): # a row number: OFFSET loc LIMIT 1 
#       row = loc
#     elif isinstance(loc, str): # a column name: Projection
#       col = loc
#     elif isinstance(loc, ColRef):
#       col = loc.column
#     elif isinstance(loc, Tuple): # row + column
#       if len(loc) != 2:
#         raise ValueError(f"Invalid length of access tuple: {len(loc)}, required: 2")

#       row = loc[0]
#       col = loc[1]
#     else:
#       raise ValueError(f"invalid parameter values to at! type: {type(loc)}")

#     result = self.df
    
#     if col:
#       result = result.project([col])
    
#     if row:
#       result = result.limit(n=1, offset=row)

#     return result.collect()

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