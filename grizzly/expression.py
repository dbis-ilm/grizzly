class ExpressionException(Exception):
  pass

class Expr(object):
  def __init__(self, left, right, opStr):
    super().__init__()
    self.left = left
    self.right = right
    self.opStr = opStr

  def __and__(self, other):
    expr = And(self, other)
    return expr

  def __or__(self, other):
    expr = Or(self, other)
    return expr

class ColRef(object):
  def __init__(self, column, df):
    # if column != "*" and not df.hasColumn(column):
    #   raise ExpressionException(f"No such column: {column}")
    self.column = column
    self.df = df

  def __str__(self):
    if self.df.alias and self.column != "*":
      s = f"{self.df.alias}.{self.column}"
    else:
      s = self.column
    return s

<<<<<<< Updated upstream

=======
  # def __eq__(self, o: object) -> bool:
  #     return isinstance(o, ColRef) and o.column == self.column
>>>>>>> Stashed changes

class Eq(Expr):
  def __init__(self, left, right):
    super().__init__(left, right, "=")
    
class Ne(Expr):
  def __init__(self, left, right):
    super().__init__(left, right, "<>")
  

class Gt(Expr):
  def __init__(self, left, right):
    super().__init__(left, right, ">")

class Ge(Expr):
  def __init__(self, left, right):
    super().__init__(left, right, ">=")

class Lt(Expr):
  def __init__(self, left, right):
    super().__init__(left, right, "<")

class Le(Expr):
  def __init__(self, left, right):
    super().__init__(left, right, "<=")
    

class And(Expr):
  def __init__(self, left, right):
    super().__init__(left, right, "and")

  def __str__(self):
    return f"({self.left}) AND ({self.right})"

class Or(Expr):
  def __init__(self, left, right):
    super().__init__(left, right, "or")

  def __str__(self):
    return f"{self.left} OR {self.right}"