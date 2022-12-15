import queue

from enum import Enum
from typing import List
class ModelType(Enum):
  TORCH = 1
  TF    = 2
  ONNX  = 3

class BooleanOperation(Enum):
  EQ = 1
  NE = 2
  GT = 3
  GE = 4
  LT = 5
  LE = 6

class ArithmeticOperation(Enum):
  ADD = 1
  SUB = 2
  MUL = 3
  DIV = 4
  MOD = 5
  POW = 6

class LogicOperation(Enum):
  AND = 1
  OR  = 2
  NOT = 3
  XOR = 4

class SetOperation(Enum):
  IN = 1

class ExpressionException(Exception):
  def __init__(self, *args: object):
      super().__init__(*args)

class Expr(object):

  @staticmethod
  def _checkRight(other):
    '''If the right hand side of an operation is not an expression or a dataframe
    we handle it as a constant
    '''

    if not other:
      return None

    import grizzly.dataframes.frame
    if isinstance(other, Expr) or isinstance(other, grizzly.dataframes.frame.DataFrame):
      return other

    return Constant(other)

  # boolean operations
  def __eq__(self, other):
    right = Expr._checkRight(other)
    expr = BoolExpr(self, right, BooleanOperation.EQ)
    return expr

  def __ne__(self, other):
    right = Expr._checkRight(other)
    expr = BoolExpr(self, right, BooleanOperation.NE)
    return expr

  def __ge__(self, other):
    right = Expr._checkRight(other)
    expr = BoolExpr(self, right, BooleanOperation.GE)
    return expr

  def __gt__(self, other):
    right = Expr._checkRight(other)
    expr = BoolExpr(self, right, BooleanOperation.GT)
    return expr

  def __le__(self, other):
    right = Expr._checkRight(other)
    expr = BoolExpr(self, right, BooleanOperation.LE)
    return expr

  def __lt__(self, other):
    right = Expr._checkRight(other)
    expr = BoolExpr(self, right, BooleanOperation.LT)
    return expr

  # logic operations
  def __and__(self, other):
    right = Expr._checkRight(other)
    expr = LogicExpr(self, right, LogicOperation.AND)
    return expr

  def __or__(self, other):
    right = Expr._checkRight(other)
    expr = LogicExpr(self, right, LogicOperation.OR)
    return expr

  def __invert__(self):
    expr = LogicExpr(self, None, LogicOperation.NOT)
    return expr

  def __xor__(self, other):
    right = Expr._checkRight(other)
    expr = LogicExpr(self, right, LogicOperation.XOR)
    return expr

  # arithmethic operations
  def __add__(self, other):
    right = Expr._checkRight(other)
    expr = ArithmExpr(self, right, ArithmeticOperation.ADD)
    return expr

  def __sub__(self, other):
    right = Expr._checkRight(other)
    expr = ArithmExpr(self, right, ArithmeticOperation.SUB)
    return expr

  def __mul__(self, other):
    right = Expr._checkRight(other)
    expr = ArithmExpr(self, right, ArithmeticOperation.MUL)
    return expr

  def __truediv__(self, other):
    right = Expr._checkRight(other)
    expr = ArithmExpr(self, right, ArithmeticOperation.DIV)
    return expr

  def __mod__(self, other):
    right = Expr._checkRight(other)
    expr = ArithmExpr(self, right, ArithmeticOperation.MOD)
    return expr

  def __pow__(self, other):
    right = Expr._checkRight(other)
    expr = ArithmExpr(self, right, ArithmeticOperation.POW)
    return expr

class BinaryExpression(Expr):
  def __init__(self, left: Expr, right: Expr, operand):
    self.left = left
    self.right = right
    self.operand = operand
    super().__init__()  

  def __hash__(self) -> int:
      return hash((self.left, self.right, self.operand))

class Constant(Expr):
  def __init__(self, value, alias: str = None):
    self.value = value
    self.alias = alias
    super().__init__()

class ArithmExpr(BinaryExpression):
  def __init__(self, left: Expr, right: Expr, operand: ArithmeticOperation):
    super().__init__(left, right, operand)

class BoolExpr(BinaryExpression):
  def __init__(self, left: Expr, right: Expr, operand: BinaryExpression):
    super().__init__(left, right, operand)

class LogicExpr(BinaryExpression):
  def __init__(self, left: Expr, right: Expr, operand: LogicOperation):
    super().__init__(left, right, operand)

class SetExpr(BoolExpr):
  def __init__(self, left: Expr, right: Expr, operand: SetOperation):
      super().__init__(left, right, operand)

class Param:
  def __init__(self, name: str, type: str):
    self.name = name
    self.type = type

  # def __str__(self):
  #   return f"{self.name}:{self.type}"

class ComputedCol(object):
  def __init__(self, value, alias = None):
    self.value = value
    self.alias = alias
    super().__init__()

class UDF(object):

  def __init__(self, name: str, params: List[Param], lines: List[str], returnType: str, lang: str=None, func=None, fallback=False):
    self.name = name
    self.params = params
    self.lines = lines
    self.returnType = returnType 
    self.lang = lang
    self.func = func
    self.fallback = fallback

  def __str__(self):
    paramString = ','.join(str(p) for p in self.params)
    return f"{self.name}({paramString}): {self.returnType}"

class ModelUDF(UDF):
  def __init__(self, name: str, params: List[Param], returnType: str, modelType:ModelType, template_replacement_dict):
    UDF.__init__(self,name, params, None, returnType, lang="py")
    self.modelType = modelType
    self.templace_replacement_dict = template_replacement_dict

class FuncCall(Expr):
  def __init__(self, funcName, inputCols: List, udf: UDF = None, alias: str = ""):
    self.funcName = funcName
    self.inputCols = inputCols
    self.udf = udf
    self.alias = alias

    super().__init__()

  # def __str__(self):
  #   cols = [f"{self.df.alias}.{c.column}" for c in self.inputCols]
  #   colsStr = ", ".join(cols)
  #   s = f"{self.funcName}({colsStr})"

  #   if self.alias != "":
  #     s += f" as {self.alias}"
    
  #   return s

class ColRef(Expr):
  def __init__(self, column: str, df, alias: str = ""):
    if not isinstance(column, str):
      raise ValueError(f"Invalid value for column: {column}")
    self.column = column
    self.alias = alias
    self.df = df

    super().__init__()

  def __str__(self):

    return f"DF: {self.df} Col:{self.column} AS: {self.alias}"

  def colName(self):
    return self.column

  def min(self):
    return self.df.min(self.column)

  def max(self):
    return self.df.max(self.column)

  def count(self):
    return self.df.count(self.column)

  def mean(self):
    return self.df.mean(self.column)

  def sum(self):
    return self.df.sum(self.column)

  ###### DF compatibility. 
  # A ColRef might be used just like a projection, thus, 
  # we mimic the DF API here and return a projection, followed by 
  # the according operation
  def __getattr__(self, name: str):
    
    if not hasattr(super(), name):
      p = self.df.project(self.column)
      return getattr(p, name)
    
    return getattr(self, name)

  def __getitem__(self, expr):
    if isinstance(expr, str):
      if expr != self.column:
        raise ExpressionException(f"invalid column reference: {expr}. Only have {self.column}")
      else:
        return self
    else:
      p = self.df.project(self.column)
      return p[expr] # use __getitem__ of DataFrame

class AllColumns(ColRef):
  def __init__(self, df):
    super().__init__('*', df)


class ExprTraverser:
  @staticmethod
  def bf(e: Expr, visitorFunc):
    todo = queue.Queue()
    todo.put_nowait(e)

    while todo.qsize() > 0:
      current = todo.get_nowait()

      if isinstance(current, BinaryExpression) and current.left:
        todo.put_nowait(current.left)
      if isinstance(current, BinaryExpression) and current.right:
        todo.put_nowait(current.right)
      
      visitorFunc(current)

  @staticmethod
  def df(e: Expr, visitorFunc):
    todo = queue.LifoQueue()
    todo.put_nowait(e)

    while todo.qsize() > 0:
      current = todo.get_nowait()

      if isinstance(current, BinaryExpression) and current.left:
        todo.put_nowait(current.left)
      if isinstance(current, BinaryExpression) and current.right:
        todo.put_nowait(current.right)
      
      visitorFunc(current)