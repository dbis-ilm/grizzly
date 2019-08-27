import frame

class Column(object):
    def __init__(self, relation, name, dtype,   table):
        self.relation = relation
        self.name = name
        self.dtype = dtype
        self.table = table

    def fqn(self):
        return f"{self.relation}.{self.name}"

    def __eq__(self, other):
        # print("eq function")
        expr = Eq(self.fqn(), other)
        
        # self.table.select(self.table.columns[self.name].__eq__(other))
        # print(str(expr))
        return expr

    def __str__(self): 
        return self.fqn()

class Expr(object):
  def __init__(self, left, right, opStr):
    super().__init__()
    self.left = left
    self.right = right
    self.opStr = opStr

  def __str__(self):
    rightSQLRep = ""
    
    if isinstance(self.right, str):
      rightSQLRep = f"'{self.right}'"
    elif isinstance(self.right, frame.DataFrame2):
      rightSQLRep = f"__RIGHTNAME__.{self.right.columns[0]}"
    else:
      rightSQLRep = self.right

    return f"{self.left} {self.opStr} {rightSQLRep}"

  def __and__(self, other):
    expr = And(self, other)
    return expr

  def __or__(self, other):
    expr = Or(self, other)
    return expr
    

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