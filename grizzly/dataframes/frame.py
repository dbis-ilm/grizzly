from grizzly.expression import Eq, Ne, Ge, Gt, Le, Lt, And, Or, Expr, ColRef
from grizzly.generator import GrizzlyGenerator
from grizzly.aggregates import AggregateType
###########################################################################
# Base DataFrame with common operations

class DataFrame(object):

  tVarCounter = 0

  @staticmethod
  def _incrAndGetTupleVar():
    tVar = f"_t{DataFrame.tVarCounter}"
    DataFrame.tVarCounter += 1
    return tVar

  def __init__(self, parents, alias):
    super(DataFrame, self).__init__()

    # self.tVar = DataFrame._incrAndGetTupleVar()
    self.alias = alias

    if parents is None or type(parents) is list:
      self.parents = parents
    else:
      self.parents = [parents]

  def filter(self, expr):
    return Filter(expr, self)

  def project(self, cols):
    return Projection(cols, self)

  def distinct(self):
    return Projection(None, self, doDistinct = True)

  def join(self, other, on, how="inner", comp = "="):
    return Join(self, other, on, how, comp)

  def groupby(self, groupCols):
    return Grouping(groupCols, self)

  ###################################
  # shortcuts

  def __getitem__(self, key):
    theType = type(key)

    if isinstance(key, Expr):
      # print(f"filter col: {key}")
      return self.filter(key)
    elif theType is str:
      # print(f"projection col: {key}")
      return self.project([ColRef(key, self)])
    elif theType is list:
      # print(f"projection list: {key}")
      return self.project([ColRef(k, self) for k in key])
    else:
      print(f"{key} has type {theType} -- ignoring")
      return self

  ###################################
  # Comparison expressions

  def __eq__(self, other):
    if not isinstance(self, Projection) or len(self.attrs) != 1:
      raise ExpressionException("Must have a projection with exactly one attribute")

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


  ###################################
  # aggregation functions
  from grizzly.aggregates import AggregateType
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
    # return self._execAgg("count",colName)
    return GrizzlyGenerator.aggregate(self, colName, AggregateType.COUNT)

  def sum(self , col):
    return GrizzlyGenerator.aggregate(self, col, AggregateType.SUM)
    # return self._execAgg("sum", col)

  ###################################
  # show functions

  def generate(self):
    return GrizzlyGenerator.generate(self)

  def show(self, pretty=False, delim=",", maxColWidth=20):
    GrizzlyGenerator.execute(self,delim,pretty,maxColWidth)
    
  def __str__(self):
    return GrizzlyGenerator.toString(self)
    
###########################################################################
# Concrete DataFrames representing an operation


class Table(DataFrame):
  def __init__(self, table):
    self.table = table
    super().__init__(None, DataFrame._incrAndGetTupleVar())

class Projection(DataFrame):

  def __init__(self, attrs, parent, doDistinct = False):
    self.attrs = attrs
    self.doDistinct = doDistinct
    super().__init__(parent, parent.alias)

class Filter(DataFrame):

  def __init__(self, expr, parent):
    self.expr = expr
    super().__init__(parent, parent.alias)
 

class Grouping(DataFrame):

  def __init__(self, groupCols, parent):
    self.groupCols = [ColRef(col, parent) for col in groupCols]
    super().__init__(parent, parent.alias)

class Join(DataFrame):

  def __init__(self, parent, other, on, how, comp):
    self.right = other
    self.on = on
    self.how = how
    self.comp = comp
    super().__init__(parent, parent.alias)