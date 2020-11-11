from grizzly.aggregates import AggregateType
from grizzly.dataframes.frame import Limit, Ordering, UDF, ModelUDF, Table, ExternalTable, Projection, Filter, Join, Grouping, DataFrame
from grizzly.expression import FuncCall, ColRef, Expr, ModelType, Or, And
from grizzly.generator import GrizzlyGenerator

from typing import List, Tuple
from pathlib import Path
import os

import logging
logger = logging.getLogger(__name__)

class Query:

  def __init__(self, generator):
    self.generator = generator
    # self.alias = alias

  def _reset(self):
    pass

  def _doExprToSQL(self, expr):
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
      exprSQL = str(expr)
      # exprSQL = f"{alias}.{expr.column}"

    elif isinstance(expr, Expr):
      l = self._doExprToSQL(expr.left)
      r = self._doExprToSQL(expr.right)

      exprSQL = f"{l} {expr.opStr} {r}"
    # right hand side is some constant (other than string), e.g. number
    else:
      exprSQL = str(expr)

    return exprSQL

  def _exprToSQL(self, expr):
    leftExpr = self._doExprToSQL(expr.left)
    rightExpr = self._doExprToSQL(expr.right)

    return f"{leftExpr} {expr.opStr} {rightExpr}"

  def _buildFrom(self,df) -> Tuple[List[str], str, str]:

    if df is not None:

      computedCols = ""
      preCode = []

      if df.computedCols:
        computedCols = ",".join(str(x) for x in df.computedCols)
        preCode = [self.generator.generateCreateFunc(call.udf) for call in df.computedCols if isinstance(call, FuncCall)]

      if isinstance(df,Table):
        proj = "*"
        if computedCols:
          proj += ","+computedCols
          
        return (preCode, f"SELECT {proj} FROM {df.table} {df.alias}")
        

      elif isinstance(df, ExternalTable):
        proj = "*"
        if computedCols:
          proj += ","+computedCols

        return (preCode + self.generator._generateCreateExtTable(df), f"SELECT {proj} FROM {df.table} {df.alias}")

      elif isinstance(df,Projection):
        subQry = Query(self.generator)
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])


        prefixed = "*"
        if df.attrs:
          prefixed = ",".join([str(attr) for attr in df.attrs])

        if computedCols:
          prefixed += ","+computedCols
        
        return (preCode + pre, f"SELECT { 'DISTINCT ' if df.doDistinct else ''}{prefixed} FROM ({parentSQL}) {df.alias}")

      elif isinstance(df,Filter):
        subQry = Query(self.generator)
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])

        exprStr = self._exprToSQL(df.expr)

        proj = "*"
        if computedCols:
          proj += ","+computedCols

        return (preCode + pre, f"SELECT {proj} FROM ({parentSQL}) {df.alias} WHERE {exprStr}")

      elif isinstance(df, Join):

        lQry = Query(self.generator)
        (lpre,lparentSQL) = lQry._buildFrom(df.leftParent())

        rQry = Query(self.generator)
        (rpre,rparentSQL) = rQry._buildFrom(df.rightParent())

        if isinstance(df.on, Or) or isinstance(df.on, And):
          lAlias = df.leftParent().alias
          rAlias = df.rightParent().alias
          onSQL = "ON " + self._exprToSQL(df.on)
        elif isinstance(df.on, Expr):
          # use the alias from the already built join condition
          lAlias = df.on.left.df.alias
          rAlias = df.on.right.df.alias
          onSQL = "ON " + self._exprToSQL(df.on)
        elif isinstance(df.on, list):
          lAlias = GrizzlyGenerator._incrAndGetTupleVar()
          rAlias = GrizzlyGenerator._incrAndGetTupleVar()
          onSQL = f"ON {lAlias}.{df.on[0]} {df.comp} {rAlias}.{df.on[1]}"
        else:
          lAlias = df.leftParent().alias
          rAlias = df.rightParent().alias
          onSQL = ""

        # joinSQL = f"{df.how} JOIN {rightSQL} {rtVar} {onSQL}"
        # self.joins.append(joinSQL)
        proj = "*"
        if computedCols:
          proj += ","+computedCols

        joinSQL = f"SELECT {proj} FROM ({lparentSQL}) {lAlias} {df.how} JOIN ({rparentSQL}) {rAlias} {onSQL}"

        return (preCode + lpre + rpre, joinSQL)

      elif isinstance(df, Grouping):
        subQry = Query(self.generator)
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])

        by = ",".join([str(attr) for attr in df.groupCols])

        funcCode = ""
        if df.aggFunc:
          (func, col) = df.aggFunc
          funcCode = ", " + SQLGenerator._getFuncCode(df, col, func)
        
        groupSQL = f"SELECT {by} {funcCode} FROM ({parentSQL}) {df.alias} GROUP BY {by}"

        if computedCols:
          tVar = GrizzlyGenerator._incrAndGetTupleVar()
          proj = "*,"+computedCols
          groupSQL = f"SELECT {proj} FROM {groupSQL} {tVar}"

        return (preCode + pre, groupSQL)

      elif isinstance(df, Limit):
        subQry = Query(self.generator)
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])

        limitClause = self.generator.templates["limit"].lower()
        limitSQL = None
        if limitClause == "top":
          limitSQL = f"SELECT TOP {df.limit} {df.alias}.* FROM ({parentSQL}) {df.alias}"
        elif limitClause == "limit":
          limitSQL = f"SELECT {df.alias}.* FROM ({parentSQL}) {df.alias} LIMIT {df.limit}"
        else:
          raise ValueError(f"Unknown keyword for LIMIT: {limitClause}")

        if df.offset > 0:
          limitSQL += f" OFFSET {df.offset}"


        return (preCode+pre, limitSQL)
      
      elif isinstance(df, Ordering):
        subQry = Query(self.generator)
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])

        by = ",".join([str(attr) for attr in df.by])
        direction = "ASC" if df.ascending else "DESC"

        qry = f"SELECT * FROM ({parentSQL}) {df.alias} ORDER BY {by} {direction}"

        return (preCode+pre, qry)

      else:
        raise ValueError(f"unsupported operator {type(df)}")

    else:
      return ""


class Config:

  @staticmethod
  def loadProfile(profile: str):
    logger.debug("loading configs for profile %s",profile)
    if not profile:
      return Config(profile, dict())

    configDir = Path.home().joinpath(".config","grizzly")
    locations = [Path.cwd(), configDir]

    confFileName = "grizzly.yml"

    path = None
    for loc in locations:
      p = loc.joinpath(confFileName)
      if p.exists():
        path = p
        logger.debug(f"found config file in: {str(path)}")
        break

    if not path: # as not found in expected locations
      logger.debug(f"Cannot find config file {confFileName} in {[str(l) for l in locations]} - creating default in {str(configDir)}...")
      # load packaged ressource
      import pkg_resources 
      my_data = pkg_resources.resource_string(__name__, "grizzly.yml").decode("utf-8") 
      
      filename = configDir.joinpath(confFileName)
      os.makedirs(os.path.dirname(filename), exist_ok=True) # create config directory
      with open(filename,'w') as target:
        target.writelines(my_data) # copy 

      logger.debug("done")
      path = filename # use below


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
    self.cnt = 0
  
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
      return "varchar(1024)"
    # elif pythonType == "long":
    #   return "bigint"
    else: 
      return pythonType

  def generateCreateFunc(self, udf: UDF) -> str:
    paramsStr = ",".join([f"{p.name} {SQLGenerator._mapTypes(p.type)}" for p in udf.params])
    returnType = SQLGenerator._mapTypes(udf.returnType)

    if isinstance(udf, ModelUDF):
      lines = self.templates[udf.modelType.name + "_code"]
      for key, value in udf.templace_replacement_dict.items():
        lines = lines.replace(key, str(value))

    else:
      lines = udf.lines[1:]
      lines = SQLGenerator._unindent(lines)
      lines = "".join(lines)

    template = self.templates["createfunction"]
    code = template.replace("$$name$$", udf.name)\
      .replace("$$inparams$$",paramsStr)\
      .replace("$$returntype$$",returnType)\
      .replace("$$code$$",lines)
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
  def _getFuncCode(df, col, func) -> str:
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

  def _generateAggCode(self, df, col, func) -> Tuple[List[str],str]:
    # aggregation over a table is performed in a way that the actual query
    # that was built is executed as an inner query and around that, we 
    # compute the aggregation
    
    if df.parents:
      (pre, innerSQL) = self.generate(df)
      df.alias = GrizzlyGenerator._incrAndGetTupleVar()
      funcCode = SQLGenerator._getFuncCode(df, col, func)
      aggSQL = f"SELECT {funcCode} FROM ({innerSQL}) as {df.alias}"
      
    else:
      funcCode = SQLGenerator._getFuncCode(df, col, func)
      aggSQL = f"SELECT {funcCode} FROM {df.table} {df.alias}"
      pre = []

    return (pre, aggSQL)

  def generate(self, df) -> Tuple[List[str],str]:
    qry = Query(self)
    (preQueryCode, qryString) = qry._buildFrom(df)

    return (preQueryCode, qryString)