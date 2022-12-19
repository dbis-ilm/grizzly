from enum import Enum
from grizzly.expression import AllColumns, ArithmExpr, BinaryExpression, BoolExpr, ColRef, ComputedCol, Constant, ExprTraverser, FuncCall, LogicExpr, SetExpr

class SchemaError(Exception):
  def __init__(self, *args: object) -> None:
    super(SchemaError, self).__init__(*args)

class ColType(Enum):
  UNKNOWN = 0

  TEXT = 1
  NUMERIC = 2
  BOOL = 3

  @staticmethod
  def fromPython(pythonType):
    if pythonType == str:
      return ColType.TEXT
    elif pythonType == int or pythonType == float:
      return ColType.NUMERIC
    elif pythonType == bool:
      return ColType.BOOL
    else: 
      return ColType.UNKNOWN
      # raise SchemaError(f"Cannot convert python type {pythonType} for internal type system")

  @staticmethod
  def fromString(typeStr):
    typeStr = typeStr.strip().lower()
    if typeStr == "str":
      return ColType.TEXT
    elif typeStr == "int" or typeStr == "float":
      return ColType.NUMERIC
    elif typeStr == "bool":
      return ColType.BOOL
    else:
      return ColType.UNKNOWN
      # raise SchemaError(f"Cannot convert type string '{typeStr}' for internal type system")


class Schema(object):
  
  cnt = 0

  def __init__(self, typeDict):
    super().__init__()

    self.typeDict = typeDict

  @staticmethod
  def build(typeDict: dict):
    newSchema = {}
    for (name,pyType) in typeDict.items():
      newSchema[name] = ColType.fromPython(pyType)

    return Schema(newSchema)

  @staticmethod
  def fromList(schemaList):
    d = {}
    for e in schemaList:
      kv = e.split(":")
      colName = kv[0]
      dtype= kv[1]

      grizzlyType = ColType.fromString(dtype)
      d[colName] = grizzlyType

    return Schema(d)

  def __len__(self):
    if self.typeDict is None:
      return 0
    else:
      return len(self.typeDict)


  def __getitem__(self, item):
    if self.typeDict is not None and item in self.typeDict:
      return self.typeDict[item]
    else:
      return ColType.UNKNOWN

  def items(self):
    if self.typeDict is None:
      return []
    else:
      return list(self.typeDict.items())

  def values(self):
    if self.typeDict is None:
      return []
    else:
      return list(self.typeDict.values())
  
  def columns(self, filterFunc = None, df = None):
    if self.typeDict is None:
      return []
    else:
      l = self.typeDict.items()
      if filterFunc is not None:
        l = filter(filterFunc, l)

      if df:
        return list(map(lambda x: ColRef(x[0], df), l)) 
      else:
        return list(map(lambda t : t[0], l))

  def check(self, item):
    if self.typeDict is None:
      return

    accessedCols = Schema._getRefs(item)

    for col in accessedCols:
      if not (isinstance(col, AllColumns) or col in self.columns()):
        raise SchemaError(f"invalid column reference: {col} not in {self.typeDict}")

  def checkType(self, col, value):
    if self.typeDict is None:
      return False

    colName = Schema._getName(col)
    if not colName in self.typeDict:
      raise SchemaError("No such column: " + colName)

    valType = Schema._inferType(value, self)
    colType = self[colName]
    return  valType == colType


  @staticmethod
  def _getRefs(item):
    if isinstance(item, str):
      return []
    elif isinstance(item, ColRef):
      return [item]
    elif isinstance(item, FuncCall):
      return item.inputCols  
    elif isinstance(item, ComputedCol):
      return Schema._getRefs(item.value)
    elif isinstance(item, Constant):
      return []
    elif isinstance(item, BinaryExpression):

      cols = []

      def collectColsAndRefs(e):
        c=cols
        if isinstance(e, ColRef):
          c.append(e)
        elif isinstance(e, FuncCall):
          c += e.inputCols

      ExprTraverser.bf(item, collectColsAndRefs)
      return cols
    else:
      # what is it?
      return []


  def __contains__(self, item):
    if self.typeDict is None:
      return True
    else:
      n = Schema._getName(item)
      return n in self.typeDict

  def __str__(self):
    return str(self.typeDict)

  def __iter__(self):
    if self.typeDict is None:
      return iter({})
    else:
      return iter(self.typeDict)

  @staticmethod
  def __genName():
    Schema.cnt += 1
    return "expr"+str(Schema.cnt)

  @staticmethod
  def _getName(ref):
    if isinstance(ref, ColRef):
      return ref.column
    elif isinstance(ref, FuncCall):
      func = ref
      if func.alias is not None and func.alias != "":
        return func.alias
      else:
        return func.funcName
    elif isinstance(ref, ComputedCol):
      if ref.alias is not None:
        return ref.alias
      else:
        return Schema.__genName()
    elif isinstance(ref, Constant):
      return str(ref.value)
    elif isinstance(ref, BinaryExpression):
      return Schema.__genName()
    else:
      return str(ref)

  def infer(self, refs):
    '''
    Tries to extract the schema based on the list of given expressions/refs
    And returns the resulting schema
    '''
    newSchemaDict = {}

    # no schema has been set until now
    # add columns with "unknown" type
    if self.typeDict is None:
      for col in refs:
        # exclude AllColumns references: our type dict is empty, thus we have no info what exists
        if not isinstance(col, AllColumns):
          name = Schema._getName(col)
          newSchemaDict[name] = ColType.UNKNOWN

    else:
      # schema was set, now get the requested columns
      for col in refs:

        # an AllColumns instance is a shortcut to request all columns
        # we can only guess from what was known from before
        if isinstance(col, AllColumns):
          for (name, dtype) in col.df.schema.typeDict.items():
            newSchemaDict[name] = dtype
        else:
          name = Schema._getName(col)
          if name in self.typeDict:
            newSchemaDict[name] = self.typeDict[name]
          else:
            # is not in parent schema -> must be a new column
            t = Schema._inferType(col, self)
            newSchemaDict[name] = t

    return Schema(newSchemaDict)
        
  def append(self,value): 
    '''
    Add a new column to this schema
    This modifies the schema in place and also returns the resulting schema
    '''  
    resultType = Schema._inferType(value, self)
    name = Schema._getName(value)
    
    if self.typeDict is None:
      # self.typeDict = {name:resultType}
      return self
    else:
      self.typeDict[name] = resultType

    return self


  def merge(self,other):
    if not isinstance(other, Schema):
      raise ValueError(f"expected an instance of schema but got {type(other)}")
    lDict = self.typeDict
    rDict = other.typeDict

    if lDict is None and rDict is None:
      return Schema(None)
    elif lDict is None and rDict is not None:
      return Schema(rDict.copy())
    elif lDict is not None and rDict is None:
      return Schema(lDict.copy())
    else: # both are not empty
      resulting = lDict.copy()
      return Schema(resulting.update(rDict))

  @staticmethod
  def _inferType(col, schema = None):
    from grizzly.dataframes.frame import DataFrame

    if isinstance(col, ColRef):
      # might happen when inferring type from function call
      # get type from schema of referenced DF
      if  col.column in schema:
        return schema[col.column]
      else:
        return ColType.UNKNOWN
        # raise SchemaError(f"{col} not in schema of df ({col.df.schema})")

    elif isinstance(col, ComputedCol):
      # CC is just a wrapper. get from its value
      return Schema._inferType(col.value)

    elif isinstance(col, FuncCall):
      # get from the function's result type
      func = col # this naming makes more sense
      if func.udf is not None:
        returnType = func.udf.returnType
        return ColType.fromString(returnType)
      else: # it must be a built-in agg func which all return numeric expect for min/max
        strFunc = str(func.funcName).strip().lower()
        if strFunc.endswith("min") or strFunc.endswith("max"):
          # get type from input col
          inputCol = func.inputCols[0]
          return Schema._inferType(inputCol, schema)
        else:
          return ColType.NUMERIC
    elif isinstance(col, Constant):
      # similar to FuncCalls, Constant's are wrappers around native Python objects
      # it's the type of the Constant's value
      return ColType.fromPython(type(col.value))
    elif isinstance(col, BoolExpr) or isinstance(col, LogicExpr):
      # a bool or logic expression returns always a boolean
      return ColType.BOOL 
    elif isinstance(col, ArithmExpr):
      return ColType.NUMERIC
    # elif isinstance(col, SetExpr) # --> SetExpr is a child of Bool expression
    elif isinstance(col, DataFrame):
      numCols = len(col.schema)
       
      if numCols > 1:
        raise SchemaError(f"can only embed DataFrames that return a single value, but {col} one has {numCols}")
      elif numCols == 1:
        return col.schema.values()[0]
      else:
        return ColType.UNKNOWN
    else:
      raise SchemaError(f"cannot handle unexpected type: {type(col)}")