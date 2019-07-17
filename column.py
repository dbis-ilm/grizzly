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
  def __init__(self):
    return super().__init__()

class Eq(Expr):
  def __init__(self, left, right):
    super().__init__()
    self.left = left
    self.right = right

  def __str__(self):
    rightSQLRep = ""
    if isinstance(self.right, str):
      rightSQLRep = f"'{self.right}'"
    else:
      rightSQLRep = self.right

    return f"{self.left} = {rightSQLRep}"