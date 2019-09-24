from .column import Expr

class SqlOp(object):
  def __init__(self, parent, name = None):
    self.parent = parent
    if not name:
      self._name = parent.name()
    else:
      self._name = name

  def name(self):
    return self._name

class From(SqlOp):
  def __init__(self, relation):
    super().__init__(None, relation)
    self.relation = relation

"""
A representation of a SQL filter operator
"""
class Filter(SqlOp):
  """
  Construct a new filter operator
  """
  def __init__(self, expr, parent):
    super().__init__(parent)
    self.expr = expr

  def __str__(self):
    return str(self.expr)

class Projection(SqlOp):
  """
  Projection to column names
  """
  def __init__(self, attrs, parent, distinct = False):
    super().__init__(parent)
    self.attrs = attrs
    self.distinct = distinct


class Grouping(SqlOp):
  """
  Grouping on columns
  """
  def __init__(self, groupcols, parent):
    super().__init__(parent)
    self.groupcols = groupcols
    self.aggFunc = None

  def setAggFunc(self, func):
    self.aggFunc = func

  def getAggFunc(self):
    return self.aggFunc
    
class Join(SqlOp):
  def __init__(self, otherDF, on, how, comp, parent):
    # assert len(on) == 2
    super().__init__(parent)
    self.otherDF = otherDF
    self.on = on
    self.how = how
    self.comp = comp

  def sql(self, leftName, rightName):
    innerSQL = self.otherDF.sql()

    onClause = ""
    if isinstance(self.on, Expr):
      onClause = str(self.on).replace("__RIGHTNAME__",rightName)
    else:
      onClause = f"{leftName}.{self.on[0]} {self.comp} {rightName}.{self.on[1]}"

    return f"{self.how.upper()} JOIN ({innerSQL}) {rightName} ON {onClause}"