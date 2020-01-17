from grizzly.expression import Eq, Ne, Ge, Gt, Le, Le, And, Or, Expr

class Table(object):
  pass

class Projection(object):
  pass

###########################################################################
# Base DataFrame with common operations

class DataFrame(object):

  def __init__(self, parents):
    super(DataFrame, self).__init__()
    if parents is None or type(parents) is list:
      self.parents = parents
    else:
      self.parents = [parents]

  def filter(self, expr):
    return Filter(expr, self)

  def project(self, cols):
    return Projection(cols, self, distinct = False)

  def distinct(self):
    return Projection(None, self, distinct = True)

  def join(self, other, on, how, comp = "="):
    return Join(self, other, on, how, comp)

  def groupby(self, groupCols):
    return Grouping(groupCols, self)

  ###################################
  # shortcuts

  def __getitem__(self, key):
    theType = type(key)

    from grizzly.expression import Expr

    if isinstance(key, Expr):
      # print(f"filter col: {key}")
      return self.filter(key)
    elif theType is str:
      # print(f"projection col: {key}")
      return self.project([key])
    elif theType is list:
      # print(f"projection list: {key}")
      return self.project(key)
    else:
      print(f"{key} has type {theType} -- ignoring")
      return self

  ###################################
  # Comparison expressions

  def __eq__(self, other):
    # print(f"eq on {self.columns[0]} and {other}")
    expr = Eq(f"{self.op.name()}.{self.columns[0]}", other)
    return expr


  def __gt__(self, other):
    expr = Gt(f"{self.op.name()}.{self.columns[0]}", other)
    return expr

  def __lt__(self, other):
    expr = Lt(f"{self.op.name()}.{self.columns[0]}", other)
    return expr

  def __ge__(self, other):
    expr = Ge(f"{self.op.name()}.{self.columns[0]}", other)
    return expr
  
  def __le__(self, other):
    expr = Le(f"{self.op.name()}.{self.columns[0]}", other)
    return expr

  def __ne__(self, other):
    expr = Ne(f"{self.op.name()}.{self.columns[0]}", other)
    return expr

  ###########################################################################
  # Actions
  ###########################################################################


  ###################################
  # aggregation functions

  def min(self, col=None):
    return self._execAgg("min",col)

  def max(self, col=None):
    return self._execAgg("max",col)

  def mean(self, col=None):
    return self._execAgg('avg',col)

  def count(self, col=None):
    colName = "*"
    if col is not None:
      colName = col
    return self._execAgg("count",colName)

  def sum(self , col=None):
    return self._execAgg("sum", col)

  ###################################
  # show functions

  def sql(self):
    from grizzly.query import Query
    qry = Query()

    curr = self
    while curr is not None:

      if isinstance(curr,Table):
        qry.table = curr.table
      elif isinstance(curr,Projection):
        if qry.projections is None:
          qry.projections = set(curr.attrs)
        else:
          qry.projections.intersection(curr.attrs)
        if curr.distinct:
          qry.distinct = "distinct"
      elif isinstance(curr,Filter):
        qry.filters.append(curr.expr)
      elif isinstance(curr, Join):
        pass

      if curr.parents is None:
        curr = None
      else:
        #TODO handle joins etc
        curr = curr.parents[0]

    return qry.sql()


###########################################################################
# Concrete DataFrames representing an operation


class Table(DataFrame):
  def __init__(self, table):
    self.table = table
    self.parents = None

  def sqlRepr(self, prefix):
    return f"{self.table} {prefix}"

class Projection(DataFrame):

  def __init__(self, attrs, parents, distinct = False):
    self.attrs = attrs
    self.distinct = distinct
    super().__init__(parents)

  def sqlRepr(self,prefix):
    prefixed = [f"{prefix}.{attr}" for attr in self.attrs]

    return ",".join(prefixed)

class Filtered(DataFrame):

  def __init__(self, expr, parents):
    self.expr = expr
    super().__init__(parents)

  def sqlRepr(self, prefix):
    return str(self.expr)

class Grouping(DataFrame):

  def __init__(self, groupCols, parents):
    self.groupCols = groupCols
    super().__init__(parents)

  def sqlRepr(self, prefix):
    prefixed = [f"{prefix}.{attr}" for attr in self.groupCols]

    return ",".join(prefixed)

class Join(DataFrame):

  def __init__(self, left, right, on, how, comp):
    self.on = on
    self.how = how
    self.comp = comp
    super().__init__([left, right])

  def sqlRepr(self, prefix):
    return f"(__LEFT__) {prefix[0]} {self.how} JOIN (__RIGHT__) {prefix[1]} ON {prefix[0]}.{self.on[0]} {self.comp} {prefix[1]}.{self.on[1]}"