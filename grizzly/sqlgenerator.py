from grizzly.aggregates import AggregateType
from grizzly.dataframes.frame import UDF, ModelUDF, Table, ExternalTable, Projection, Filter, Join, Grouping, DataFrame
from grizzly.expression import FuncCall, ColRef, Expr
from typing import List
from grizzly.generator import GrizzlyGenerator

import random
import string
import inspect

class Query:

  def __init__(self, generator, alias: str):
    self.generator = generator
    self.alias = alias

  def _reset(self):
    pass

  def _doExprToSQL(self, expr, alias: str):
    exprSQL = ""
    # right hand side is a string constant
    if isinstance(expr, str):
      exprSQL = f"'{expr}'"
    # right hand side is a dataframe (i.e. subquery)
    elif isinstance(expr, DataFrame): 
      # if right hand side is a DataFrame, we need to create code first 
      subQry = Query(self.generator, GrizzlyGenerator._incrAndGetTupleVar())
      (pre,exprSQL) = subQry._buildFrom(expr)

    elif isinstance(expr, ColRef):
      expr.df.alias = alias
      exprSQL = str(expr)

    elif isinstance(expr, Expr):
      l = self._doExprToSQL(expr.left, alias)
      r = self._doExprToSQL(expr.right, alias)

      exprSQL = f"{l} {expr.opStr} {r}"
    # right hand side is some constant (other than string), e.g. number
    else:
      exprSQL = str(expr)

    return exprSQL

  def _exprToSQL(self, expr, alias: str):
    leftExpr = self._doExprToSQL(expr.left, alias)
    rightExpr = self._doExprToSQL(expr.right, alias)

    return f"{leftExpr} {expr.opStr} {rightExpr}"

  def _buildFrom(self,df):

    if df is not None:

      if isinstance(df,Table):
        return ([], f"SELECT * FROM {df.table} {self.alias}")
        

      elif isinstance(df, ExternalTable):
        return ([self.generator._generateCreateExtTable(df)], f"SELECT * FROM {df.table} {self.alias}")

      elif isinstance(df,Projection):
        subQry = Query(self.generator, GrizzlyGenerator._incrAndGetTupleVar())
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])


        prefixed = "*"
        if df.attrs:
          prefixed = ",".join([str(attr) for attr in df.attrs])
        
        return (pre, f"SELECT {'DISTINCT' if df.doDistinct else ''} {prefixed} FROM ({parentSQL}) {self.alias}")

      elif isinstance(df,Filter):
        subQry = Query(self.generator, GrizzlyGenerator._incrAndGetTupleVar())
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])

        exprStr = self._exprToSQL(df.expr, subQry.alias)

        return (pre, f"SELECT * FROM ({parentSQL}) {self.alias} WHERE {exprStr}")

      elif isinstance(df, Join):

        lQry = Query(self.generator, GrizzlyGenerator._incrAndGetTupleVar())
        (lpre,lparentSQL) = subQry._buildFrom(df.parents[0])

        rQry = Query(self.generator, GrizzlyGenerator._incrAndGetTupleVar())
        (rpre,rparentSQL) = subQry._buildFrom(df.right)

        if isinstance(df.on, Expr):
          onSQL = "ON " + self._exprToSQL(df.on)
        elif isinstance(df.on, list):
          onSQL = f"ON {df.alias}.{df.on[0]} {df.comp} {rtVar}.{df.on[1]}"
        else:
          onSQL = ""

        # joinSQL = f"{df.how} JOIN {rightSQL} {rtVar} {onSQL}"
        # self.joins.append(joinSQL)

        joinSQL = f"SELECT * FROM ({lparentSQL}) {lQry.alias} {df.how} JOIN ({rparentSQL}) {rQry.alias} {onSQL}"

        return (lpre.extend(rpre), joinSQL)

      elif isinstance(df, Grouping):
        subQry = Query(self.generator, GrizzlyGenerator._incrAndGetTupleVar())
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])

        groupcols = ",".join([str(attr) for attr in df.groupCols])

        funcCode = ""
        if df.aggFunc:
          (func, col) = df.aggFunc
          funcCode = ", " + SQLGenerator._getFuncCode(df, col, func)
        
        groupSQL = f"SELECT {groupcols} {funcCode} FROM ({parentSQL}) {self.alias} GROUP BY {groupcols}"

        return (pre, groupSQL)
      
      else:
        raise ValueError(f"unsupported operator {type(df)}")

    else:
      return ""


class Config:

  @staticmethod
  def loadProfile(profile: str):

    if not profile:
      return Config(profile, dict())

    path = f"./grizzly.yml"
    import yaml
    configs = None
    with open(path,"r") as configFile:
      configs = yaml.load(configFile, Loader=yaml.FullLoader)

    return Config(profile, configs[profile])


  def __init__(self, profile, config):
    self.profile = profile
    self.config = config

  def __getitem__(self, key: str):
    if key in self.config:
      return self.config[key]
    else:
      raise ValueError(f"Unsupported configuration key {key} in profile {self.profile}")


from typing import NewType
SqlBigInt = NewType("bigint", int)


class SQLGenerator:

  def __init__(self, profile: str = None):
    self.profile = profile
    self.templates = Config.loadProfile(profile)
  
  @staticmethod
  def _unindent(lines: list) -> list:
    firstLine = lines[0]

    numLeadingSpaces = len(firstLine) - len(firstLine.lstrip())
    resultLines = []
    for line in lines:
      resultLines.append(line[numLeadingSpaces:])

    return resultLines

  @staticmethod
  def _mapTypes(pythonType: str) -> str:
    if pythonType == "str":
      return "varchar(255)"
    # elif pythonType == "long":
    #   return "bigint"
    else: 
      return pythonType

  def generateCreateFunc(self, udf: UDF) -> str:
    paramsStr = ",".join([f"{p.name} {SQLGenerator._mapTypes(p.type)}" for p in udf.params])
    returnType = SQLGenerator._mapTypes(udf.returnType)

    modelCode = ""
    modelClassName = ""

    if isinstance(udf, ModelUDF):
      helperCode = "\n"
      for helperFunc in udf.helpers:
        (funcLines,_) = inspect.getsourcelines(helperFunc)
        funcLines = SQLGenerator._unindent(funcLines)
        helperCode += "".join(funcLines)

      (encoderCode,_) = inspect.getsourcelines(udf.encoder)
      encoderCode = SQLGenerator._unindent(encoderCode)
      encoderCode = "".join(encoderCode)

      theHash = str(abs(udf.pathHash))

      converter = lambda x: f"\"{x}\"" if type(x) == str else f"{x}"

      outDictCode = "[" + ",".join(map(converter, udf.outputDict )) + "]"

      modelParameters = ",".join(map(converter, udf.classParameters)) if udf.classParameters else ""

      lines = self.templates["applymodelfunction"]
      lines = lines.replace("$$modelpathhash$$", theHash).replace("$$modelpath$$", udf.path).replace("$$encoderfuncname$$",udf.encoder.__name__)
      lines = lines.replace("$$helpers$$",helperCode).replace("$$encoder$$",encoderCode).replace("$$inputcols$$",paramsStr)
      lines = lines.replace("$$outputdict$$",outDictCode).replace("$$modelclassparameters$$",modelParameters)

      modelCode += udf.classCode

    else:
      lines = udf.lines[1:]
      lines = SQLGenerator._unindent(lines)
      lines = "".join(lines)

    template = self.templates["createfunction"]
    
    code = template.replace("$$name$$", udf.name).replace("$$inparams$$",paramsStr).replace("$$returntype$$",returnType).replace("$$code$$",lines)

    if modelCode != "":
      code = code.replace("$$modelclassname$$",udf.modelClassName).replace("$$modelclassdef$$",modelCode)
    return code

  def _generateCreateExtTable(self, tab: ExternalTable) -> List[str]:
    queries = []

    # In place string replacement
    for i in range(len(tab.colDefs)):
      tab.colDefs[i] = tab.colDefs[i].replace(":", " ").replace("str", "VARCHAR(1024)")
    schemaString = ",".join(tab.colDefs)

    formatString = ""
    if tab.format != "":
        formatString += f", FORMAT='{tab.format}'"

    options = [f"'delimiter'='{tab.delimiter}'"]
    if not tab.hasHeader:
      options.append("'header'='false'")
      options.append(f"'schema'='{schemaString}'")
    optionString = f""", OPTIONS=({",".join(options)})"""

    template = self.templates["externaltable"]
    code = template.replace("$$name$$", tab.table)\
      .replace("$$schema$$", schemaString)\
      .replace("$$filenames$$", tab.filenames)\
      .replace("$$format$$", formatString)\
      .replace("$$options$$", optionString)

    queries.append(f"DROP TABLE IF EXISTS {tab.table}")
    queries.append(code)
    return queries

  @staticmethod
  def _getFuncCode(df, col, func):
    if not isinstance(col, ColRef):
      colName = ColRef(col, df)
    else:
      colName = col
    
    if func == AggregateType.MEAN:
      funcStr = "avg"
    else:
      funcStr = str(func).lower()[len("aggregatetype."):]

    funcCode = f"{funcStr}({colName})"
    return funcCode

  def _generateAggCode(self, df, col, func) -> (List[str],str):
    # aggregation over a table is performed in a way that the actual query
    # that was built is executed as an inner query and around that, we 
    # compute the aggregation
    pre = []
    if df.parents:
      (pre, innerSQL) = self.generate(df)
      df.alias = GrizzlyGenerator._incrAndGetTupleVar()
      funcCode = SQLGenerator._getFuncCode(df, col, func)
      aggSQL = f"SELECT {funcCode} FROM ({innerSQL}) as {df.alias}"
      # aggSQL = innerSQL
    else:
      funcCode = SQLGenerator._getFuncCode(df, col, func)
      aggSQL = f"SELECT {funcCode} FROM {df.table} {df.alias}"

    return (pre, aggSQL)

  def generate(self, df) -> (List[str],str):
    qry = Query(self,GrizzlyGenerator._incrAndGetTupleVar())
    (preQueryCode, qryString) = qry._buildFrom(df)

    return (preQueryCode, qryString)