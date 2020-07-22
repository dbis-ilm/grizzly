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

class Param:
  def __init__(self, name: str, type: str):
    self.name = name
    self.type = type

  def __str__(self):
    return f"{self.name}:{self.type}"

class UDF(Expr):

  def __init__(self, name: str, params: list, lines: list, returnType: str):
    self.name = name
    self.params = params
    self.lines = lines
    self.returnType = returnType 

  def __str__(self):
    paramString = ','.join(str(p) for p in self.params)
    return f"{self.name}({paramString}): {self.returnType}"

class ColRef(object):
  def __init__(self, column, df, alias: str = ""):
    # if column != "*" and not df.hasColumn(column):
    #   raise ExpressionException(f"No such column: {column}")
    self.column = column
    self.df = df
    self.alias = alias

  def __str__(self):
    if self.df.alias and self.column != "*":
      s = f"{self.df.alias}.{self.column}"
    else:
      s = self.column
    
    if self.alias != "":
      s += f" as {self.alias}"
    
    return s

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