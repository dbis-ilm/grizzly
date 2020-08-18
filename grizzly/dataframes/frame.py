from grizzly.expression import Eq, Ne, Ge, Gt, Le, Lt, And, Or, Expr, ColRef, FuncCall, ExpressionException
from grizzly.generator import GrizzlyGenerator
from grizzly.aggregates import AggregateType
from grizzly.expression import ModelUDF,UDF, Param

import inspect

###########################################################################
# Base DataFrame with common operations

class DataFrame(object):

  def __init__(self, columns, parents, alias):
    super(DataFrame, self).__init__()

    self.alias = alias
    self.columns = columns
    self.computedCols = []

    if parents is None or type(parents) is list:
      self.parents = parents
    else:
      self.parents = [parents]

  def hasColumn(self, colName):
    if not self.columns:
      return True

    for ref in self.columns:
      if ref.column == colName:
        return True

    return False

  def setAlias(self, newAlias):
    if self.columns:
      for c in self.columns:
        c.df.alias = newAlias

    self.alias = newAlias

  def filter(self, expr):
    return Filter(expr, self)

  def project(self, cols):
    return Projection(cols, self)

  def distinct(self):
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

  

  def map(self, func):
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

      (lines,_) = inspect.getsourcelines(func)
      # lines = lines[1:]
      returns = sig.return_annotation.__name__
      # returns = DataFrame._mapTypes(returns)

      # print(f"{funcName} has {len(lines)} lines and {len(params)} parameters and returns {returns}")

      udf = UDF(funcName, params, lines, returns)
      call = FuncCall(funcName, self.attrs, self, udf)

      return self.project([call])

    elif isinstance(func, DataFrame):
      return self.join(func,None, how = "natural")
    else:
      print(f"error: {func} is not a function or other DataFrame")
      exit(1)

  def predict(self, path: str, toTensorFunc, clazz, outputDict, clazzParameters: list, n_predictions: int = 1, *helperFuncs):

    if not isinstance(self, Projection):
      ValueError("classification can only be applied to a projection")

    (clazzCodeLst,_) = inspect.getsourcelines(clazz)

    clazzCode = "".join(clazzCodeLst)

    modelPathHash = abs(hash(path))
    funcName = f"grizzly_predict_{modelPathHash}"
    attrsString = "_".join([r.column for r in self.attrs])

    sig = inspect.signature(toTensorFunc)
    fparams = sig.parameters
    if len(fparams) != 1:
      raise ValueError("toTensor converter must have exactly one parameter")

    toTensorInputType = sig.parameters[list(sig.parameters)[0]].annotation.__name__

    if len(outputDict) <= 0:
      raise ValueError("output dict must not be empty")
    #predictedType = type(outputDict[0]).__name__
    predictedType = "str" # hard coded string because we collect n predictions in a list of strings

    udf = ModelUDF(funcName,[Param("invalue", toTensorInputType), Param("n_predictions", "int")], predictedType, path, modelPathHash, toTensorFunc, outputDict, list(helperFuncs),clazz.__name__, clazzCode, clazzParameters)
    call = FuncCall(funcName, self.attrs + [n_predictions] , self,udf, f"predicted_{attrsString}")

    return self.project([call])

  ###################################
  # shortcuts

  def __getattr__(self, name):
    return self.project([ColRef(name, self)])

  # magic function for write access by index: []
  def __setitem__(self, key, value):
    if isinstance(value, Projection):
      value.attrs[0].alias = key
      newCol = value.attrs[0]
    else:
      newCol = ColRef(value, self, key)
    
    self.computedCols += [newCol]



  # magic function for read access by index: []
  def __getitem__(self, key):
    theType = type(key)

    if isinstance(key, Expr):
      # print(f"filter col: {key}")
      return self.filter(key)
    elif theType is str:
      # print(f"projection col: {key}")
      return self.project([ColRef(key, self)])
    elif theType is Projection:
      return self.project([key.attrs[0]])
    elif theType is list:
      
      projList = []
      for e in key:
        t = type(e)
        if t is str:
          projList.append(ColRef(e, self))
        elif t is Projection:
          projList.append(e.attrs[0])
        else:
          raise ExpressionException(f"expected a column name string or projection, but got {e}")

      return self.project(projList)
    else:
      print(f"{key} has type {theType} -- ignoring")
      return self

  ###################################
  # Comparison expressions

  def __eq__(self, other):
    if not isinstance(self, Projection) or len(self.attrs) != 1:
      raise ExpressionException(f"Must have a projection with exactly one attribute. Got {type(self)}")

    if isinstance(other, DataFrame):
      r = other.attrs[0]
    else:
      r = other

    expr = Eq(self.attrs[0], r)
    return expr

  def __gt__(self, other):
    if not isinstance(self, Projection) or len(self.attrs) != 1:
      raise ExpressionException("Must have a projection with exactly one attribute")

    if isinstance(other, DataFrame):
      r = other.attrs[0]
    else:
      r = other

    expr = Gt(self.attrs[0], r)
    return expr

  def __lt__(self, other):
    if not isinstance(self, Projection) or len(self.attrs) != 1:
      raise ExpressionException("Must have a projection with exactly one attribute")

    if isinstance(other, DataFrame):
      r = other.attrs[0]
    else:
      r = other

    expr = Lt(self.attrs[0], r)
    return expr

  def __ge__(self, other):
    if not isinstance(self, Projection) or len(self.attrs) != 1:
      raise ExpressionException("Must have a projection with exactly one attribute")

    if isinstance(other, DataFrame):
      r = other.attrs[0]
    else:
      r = other

    expr = Ge(self.attrs[0], r)
    return expr
  
  def __le__(self, other):
    if not isinstance(self, Projection) or len(self.attrs) != 1:
      raise ExpressionException("Must have a projection with exactly one attribute")

    if isinstance(other, DataFrame):
      r = other.attrs[0]
    else:
      r = other

    expr = Le(self.attrs[0], r)
    return expr

  def __ne__(self, other):
    if not isinstance(self, Projection) or len(self.attrs) != 1:
      raise ExpressionException("Must have a projection with exactly one attribute")

    if isinstance(other, DataFrame):
      r = other.attrs[0]
    else:
      r = other

    expr = Ne(self.attrs[0], r)
    return expr

  ###########################################################################
  # Actions
  ###########################################################################

  def collect(self, includeHeader = False):
    return GrizzlyGenerator.collect(self, includeHeader)

  ###################################
  # aggregation functions
  
  def min(self, col=None):
    # return self._execAgg("min",col)
    return GrizzlyGenerator.aggregate(self, col, AggregateType.MIN)

  def max(self, col=None):
    # return self._execAgg("max",col)
    return GrizzlyGenerator.aggregate(self, col, AggregateType.MAX)

  def mean(self, col=None):
    # return self._execAgg('avg',col)
    return GrizzlyGenerator.aggregate(self, col, AggregateType.MEAN)

  def count(self, col=None):
    colName = "*"
    if col is not None:
      colName = col
    
    return GrizzlyGenerator.aggregate(self, colName, AggregateType.COUNT)

  def _gen_count(self, col=None):
    colName = "*"
    if col is not None:
      colName = col
    
    return GrizzlyGenerator._gen_aggregate(self, colName, AggregateType.COUNT)


  def sum(self , col):
    return GrizzlyGenerator.aggregate(self, col, AggregateType.SUM)
    # return self._execAgg("sum", col)

  ###################################
  # show functions

  def generate(self):
    return GrizzlyGenerator.generate(self)
  
  def generateQuery(self):
    (pre,qry) = self.generate()
    prequeries = ";".join(pre)
    return f"{prequeries} {qry}"

  def show(self, pretty=False, delim=",", maxColWidth=20, limit=20):
    print(GrizzlyGenerator.toString(self,delim,pretty,maxColWidth,limit))
    
  def __str__(self):
    # strRep = GrizzlyGenerator.toString(self, pretty=True)
    tableStr = GrizzlyGenerator.table(self)
    return tableStr
    
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

  def __init__(self, attrs, parent, doDistinct = False):
    if attrs and not (isinstance(attrs[0], ColRef) or isinstance(attrs[0], FuncCall)):
      self.attrs = [ColRef(attr, parent) for attr in attrs]
    else:
      self.attrs = attrs

    self.doDistinct = doDistinct
    super().__init__(self.attrs, parent, parent.alias)

class Filter(DataFrame):

  def __init__(self, expr, parent):
    super().__init__(parent.columns, parent, parent.alias)
    self.expr = expr
 

class Grouping(DataFrame):

  def __init__(self, groupCols, parent):
    if not isinstance(groupCols[0], ColRef):
      self.groupCols = [ColRef(col, parent) for col in groupCols]
    else:
      self.groupCols = groupCols
    
    self.aggFunc = None

    super().__init__(self.groupCols, parent, parent.alias)

  def agg(self, aggType, col):
    self.aggFunc = (aggType, col)
    return self

class Join(DataFrame):
  def __init__(self, parent, other, on, how, comp):
    super().__init__(parent.columns.extend(other.columns), parent, parent.alias)
    self.right = other
    self.on = on
    self.how = how
    self.comp = comp
