class SqlOp(object):
  def __init__(self, parent):
    self.parent = parent

class From(SqlOp):
  def __init__(self, relation):
    super().__init__(None)
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
  def __init__(self, attrs, parent):
    super().__init__(parent)
    self.attrs = attrs


class Grouping(SqlOp):
  def __init__(self, groupcols, parent):
    super().__init__(parent)
    self.groupcols = groupcols
    self.aggFunc = None

  def setAggFunc(self, func):
    self.aggFunc = func

  def getAggFunc(self):
    return self.aggFunc
    
