from grizzly.aggregates import AggregateType
from grizzly.dataframes.frame import Limit, Ordering, UDF, ModelUDF, Table, ExternalTable, Projection, Filter, Join, Grouping, DataFrame
from grizzly.expression import ComputedCol, FuncCall, ColRef, Expr, ModelType, Or, And
from grizzly.generator import GrizzlyGenerator

from typing import List, Tuple
from pathlib import Path
import os

import logging
logger = logging.getLogger(__name__)

class Query:

  def __init__(self, generator):
    self.generator = generator

  def _buildFrom(self,df) -> Tuple[List[str], str, str]:

    if df is not None:

      computedCols = []
      preCode = []

      for x in df.computedCols:
        (exprPre, exprSQL) = SQLGenerator._exprToSQL(x)
        preCode += exprPre
        computedCols.append(exprSQL)

      computedCols = ",".join(computedCols)
      preCode = [self.generator.generateCreateFunc(call.udf) for call in df.computedCols if isinstance(call, FuncCall)]

      if isinstance(df,Table):
        proj = "*"
        if computedCols:
          proj += ","+computedCols
          
        return (preCode, f"SELECT {proj} FROM {df.table} {df.id}")
        

      elif isinstance(df, ExternalTable):
        proj = "*"
        if computedCols:
          proj += ","+computedCols

        return (preCode + SQLGenerator._generateCreateExtTable(df), f"SELECT {proj} FROM {df.table} {df.id}")

      elif isinstance(df,Projection):
        subQry = Query(self.generator)
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])


        prefixed = "*"
        if df.columns:
          prefixed = []
          for (ePre, exprSQL) in [SQLGenerator._exprToSQL(attr) for attr in df.columns]:
            pre += ePre
            prefixed.append(exprSQL)
          
          prefixed = ",".join(prefixed)

        if computedCols:
          prefixed += ","+computedCols
        
        return (preCode + pre, f"SELECT { 'DISTINCT ' if df.doDistinct else ''}{prefixed} FROM ({parentSQL}) {df.id}")

      elif isinstance(df,Filter):
        subQry = Query(self.generator)
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])

        (exprPre,exprStr) = SQLGenerator._exprToSQL(df.expr)

        proj = "*"
        if computedCols:
          proj += ","+computedCols

        return (preCode + pre + exprPre, f"SELECT {proj} FROM ({parentSQL}) {df.id} WHERE {exprStr}")

      elif isinstance(df, Join):

        lQry = Query(self.generator)
        (lpre,lparentSQL) = lQry._buildFrom(df.leftParent())

        rQry = Query(self.generator)
        (rpre,rparentSQL) = rQry._buildFrom(df.rightParent())

        if isinstance(df.on, Or) or isinstance(df.on, And):
          lAlias = df.leftParent().id
          rAlias = df.rightParent().id
          (exprPre, onSQL) = SQLGenerator._exprToSQL(df.on)
          onSQL = "ON " + onSQL
          rpre += exprPre
        elif isinstance(df.on, Expr):
          # use the alias from the already built join condition
          lAlias = df.on.left.df.id
          rAlias = df.on.right.df.id
          (exprPre, onSQL) = SQLGenerator._exprToSQL(df.on)
          onSQL = "ON " + onSQL
          rpre += exprPre
        elif isinstance(df.on, list):
          lAlias = GrizzlyGenerator._incrAndGetTupleVar()
          rAlias = GrizzlyGenerator._incrAndGetTupleVar()
          onSQL = f"ON {lAlias}.{df.on[0]} {df.comp} {rAlias}.{df.on[1]}"
        else:
          lAlias = df.leftParent().id
          rAlias = df.rightParent().id
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

        byCols = []
        for attr in df.groupCols:
          (exprPre, exprSQL) = SQLGenerator._exprToSQL(attr)
          pre += exprPre
          byCols.append(exprSQL)

        by = ",".join(byCols)

        # by = ",".join([SQLGenerator._exprToSQL(attr) for attr in df.groupCols])

        funcCode = ""
        for (func, col, alias) in df.aggFunc:
          # a = f" as {alias}" if alias else ""
          funcCode += ", " + SQLGenerator._getFuncCode(df, col, func, alias)
        
        groupSQL = f"SELECT {by} {funcCode} FROM ({parentSQL}) {df.id} GROUP BY {by}"

        havings = []
        if df.having:
          for h in df.having:
            (hPre,hSQL) = SQLGenerator._exprToSQL(h)
            pre += hPre
            havings.append(hSQL)

          exprStr = " AND ".join(havings)
          groupSQL += f" HAVING {exprStr}"

        #if the computed column is an aggregate over the groups, 
        # it should not be added as an extra query, but rather 
        # merged into this projection list
        if computedCols: 
          tVar = GrizzlyGenerator._incrAndGetTupleVar()
          proj = "*,"+computedCols
          groupSQL = f"SELECT {proj} FROM {groupSQL} {tVar}"

        return (preCode + pre, groupSQL)

      elif isinstance(df, Limit):
        subQry = Query(self.generator)
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])

        limitClause = SQLGenerator.templates["limit"].lower()
        limitSQL = None
        if limitClause == "top":
          limitSQL = f"SELECT TOP {df.limit} {df.id}.* FROM ({parentSQL}) {df.id}"
        elif limitClause == "limit":
          limitSQL = f"SELECT {df.id}.* FROM ({parentSQL}) {df.id} LIMIT {df.limit}"
        else:
          raise ValueError(f"Unknown keyword for LIMIT: {limitClause}")

        if df.offset > 0:
          limitSQL += f" OFFSET {df.offset}"


        return (preCode+pre, limitSQL)
      
      elif isinstance(df, Ordering):
        subQry = Query(self.generator)
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])

        by = []
        for attr in df.by:
          (exprPre, exprSQL) = SQLGenerator._exprToSQL(attr)
          pre += exprPre
          by.append(exprSQL)

        by = ",".join(by)
        direction = "ASC" if df.ascending else "DESC"

        qry = f"SELECT * FROM ({parentSQL}) {df.id} ORDER BY {by} {direction}"

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
      super().__init__()
      SQLGenerator.init(profile)

  @staticmethod
  def init(profile):
    # self.profile = profile
    SQLGenerator.templates = Config.loadProfile(profile)
    # self.cnt = 0
  
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

  @staticmethod
  def _exprToSQL(expr) -> Tuple[list[str], str]:
    exprSQL = ""
    pre = []
    # right hand side is a string constant
    if isinstance(expr, str):
      exprSQL = f"'{expr}'"
    # right hand side is a dataframe (i.e. subquery)
    elif isinstance(expr, DataFrame): 
      # if right hand side is a DataFrame, we need to create code first 
      subQry = Query(SQLGenerator())
      (pre,exprSQL) = subQry._buildFrom(expr)

    elif isinstance(expr, ColRef):
      if expr.df and expr.column != "*":
        exprSQL = f"{expr.df.id}.{expr.column}"
      else:
        exprSQL = expr.column

      if expr.alias:
        exprSQL += f" as {expr.alias}"

    elif isinstance(expr, ComputedCol):
      (pre,exprSQL) = SQLGenerator._exprToSQL(expr.value)
      exprSQL += f" as {expr.colname}"      

    elif isinstance(expr, FuncCall):
      if expr.udf:
        pre = [SQLGenerator.generateCreateFunc(expr.udf)]
      exprSQL = SQLGenerator._getFuncCode(expr.df, expr.inputCols[0],expr.funcName, expr.alias)

    elif isinstance(expr, Expr):
      (lPre,l) = SQLGenerator._exprToSQL(expr.left)
      (rPre,r) = SQLGenerator._exprToSQL(expr.right)

      exprSQL = f"{l} {expr.opStr} {r}"
      pre = lPre + rPre
    # right hand side is some constant (other than string), e.g. number
    else:
      exprSQL = str(expr)

    return (pre,exprSQL)


  @staticmethod
  def generateCreateFunc(udf: UDF) -> str:
    paramsStr = ",".join([f"{p.name} {SQLGenerator._mapTypes(p.type)}" for p in udf.params])
    returnType = SQLGenerator._mapTypes(udf.returnType)

    if isinstance(udf, ModelUDF):
      lines = SQLGenerator.templates[udf.modelType.name + "_code"]
      for key, value in udf.templace_replacement_dict.items():
        lines = lines.replace(key, str(value))

    else:
      lines = udf.lines[1:]
      lines = SQLGenerator._unindent(lines)
      lines = "".join(lines)

    template = SQLGenerator.templates["createfunction"]
    code = template.replace("$$name$$", udf.name)\
      .replace("$$inparams$$",paramsStr)\
      .replace("$$returntype$$",returnType)\
      .replace("$$code$$",lines)
    return code

  @staticmethod
  def _generateCreateExtTable(tab: ExternalTable) -> List[str]:
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

    template = SQLGenerator.templates["externaltable"]
    code = template.replace("$$name$$", tab.table)\
      .replace("$$schema$$", schemaString)\
      .replace("$$filenames$$", tab.filenames)\
      .replace("$$format$$", formatString)\
      .replace("$$options$$", optionString)

    queries.append(f"DROP TABLE IF EXISTS {tab.table}")
    queries.append(code)
    return queries

  @staticmethod
  def _getFuncCode(df, col, func, alias = None) -> str:
    if not isinstance(col, ColRef) and col != "*":
      colName = ColRef(col, df)
    else:
      colName = col
    (_,colName) = SQLGenerator._exprToSQL(colName)


    if func == AggregateType.MEAN:
      funcStr = "avg"
    elif str(func).lower().startswith("aggregatetype."):
      funcStr = str(func).lower()[len("aggregatetype."):]
    else:
      funcStr = func

    funcCode = f"{funcStr}({colName})"

    if alias is not None:
      funcCode += f" as {alias}"

    return funcCode

  def _generateAggCode(self, df, col, func, alias) -> Tuple[List[str],str]:
    # aggregation over a table is performed in a way that the actual query
    # that was built is executed as an inner query and around that, we 
    # compute the aggregation
    
    if df.parents:
      (pre, innerSQL) = self.generate(df)
      df.alias = GrizzlyGenerator._incrAndGetTupleVar()
      funcCode = SQLGenerator._getFuncCode(df, col, func, alias)
      aggSQL = f"SELECT {funcCode} FROM ({innerSQL}) as {df.id}"
      
    else:
      funcCode = SQLGenerator._getFuncCode(df, col, func)
      aggSQL = f"SELECT {funcCode} FROM {df.table} {df.id}"
      pre = []

    return (pre, aggSQL)

  def generate(self, df) -> Tuple[List[str],str]:
    qry = Query(self)
    (preQueryCode, qryString) = qry._buildFrom(df)

    return (preQueryCode, qryString)
