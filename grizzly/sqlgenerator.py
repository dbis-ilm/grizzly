from grizzly.aggregates import AggregateType
from grizzly.dataframes.frame import Limit, Ordering, UDF, ModelUDF, Table, ExternalTable, Projection, Filter, Join, Grouping, DataFrame
from grizzly.expression import ArithmExpr, ArithmeticOperation, BoolExpr, BooleanOperation, ComputedCol, Constant, ExpressionException, FuncCall, ColRef, LogicExpr, LogicOperation, SetExpr, SetOperation
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
        (exprPre, exprSQL) = self.generator._exprToSQL(x)
        preCode += exprPre
        computedCols.append(exprSQL)

      computedCols = ",".join(computedCols)

      if isinstance(df,Table):
        proj = "*"
        if computedCols:
          proj += ","+computedCols
          
        return (preCode, f"SELECT {proj} FROM {df.table} {df.alias}")
        

      elif isinstance(df, ExternalTable):
        proj = "*"
        if computedCols:
          proj += ","+computedCols

        tablePre = SQLGenerator._generateCreateExtTable(df, self.generator.templates)
        qry = f"SELECT {proj} FROM {df.table} {df.alias}"

        return (preCode + tablePre, qry)

      elif isinstance(df,Projection):
        subQry = Query(self.generator)
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])

        prefixed = "*"
        if df.columns:
          prefixed = []

          for attr in df.columns:
            (ePre, exprSQL) = self.generator._exprToSQL(attr)

            pre += ePre
            prefixed.append(exprSQL)
          
          prefixed = ",".join(prefixed)

        if computedCols:
          prefixed += ","+computedCols

        qry = f"SELECT { 'DISTINCT ' if df.doDistinct else ''}{prefixed} FROM ({parentSQL}) {df.alias}"
        
        return (preCode + pre, qry)

      elif isinstance(df,Filter):
        subQry = Query(self.generator)
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])

        (exprPre,exprStr) = self.generator._exprToSQL(df.expr)

        proj = "*"
        if computedCols:
          proj += ","+computedCols

        qry = f"SELECT {proj} FROM ({parentSQL}) {df.alias} WHERE {exprStr}"

        return (preCode + pre + exprPre, qry)

      elif isinstance(df, Join):

        lQry = Query(self.generator)
        (lpre,lparentSQL) = lQry._buildFrom(df.leftParent())

        rQry = Query(self.generator)
        (rpre,rparentSQL) = rQry._buildFrom(df.rightParent())

        lAlias = df.leftParent().alias
        rAlias = df.rightParent().alias

        if isinstance(df.on, ColRef):
          (exprPre, onSQL) = self.generator._exprToSQL(df.on)
          onSQL = f"USING ({onSQL})"
          preCode += exprPre
        elif isinstance(df.on, LogicExpr) or isinstance(df.on, BoolExpr):
          (exprPre, onSQL) = self.generator._exprToSQL(df.on)
          onSQL = "ON " + onSQL
          preCode += exprPre
        elif isinstance(df.on, list):

          if len(df.on) != 2:
            raise ExpressionException("on condition must consist of exacltly two columns")

          (lOnPre,lOn) = self.generator._exprToSQL(df.on[0])
          (rOnPre,rOn) = self.generator._exprToSQL(df.on[1])

          onSQL = f"ON {lOn} {df.comp} {rOn}"
          preCode += lOnPre
          preCode += rOnPre
        else:
          onSQL = "" # let the DB figure it out itself

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
          (exprPre, exprSQL) = self.generator._exprToSQL(attr)
          pre += exprPre
          byCols.append(exprSQL)

        by = ",".join(byCols)

        funcCode = ""
        for f in df.aggFunc:
          (fPre,fCode) = self.generator._generateFuncCall(f)
          pre += fPre
          funcCode += ", " + fCode
        
        groupSQL = f"SELECT {by} {funcCode} FROM ({parentSQL}) {df.alias} GROUP BY {by}"

        havings = []
        if df.having:
          for h in df.having:
            (hPre,hSQL) = self.generator._exprToSQL(h)
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

        limitClause = self.generator.templates["limit"].lower()

        (lPre,limitExpr) = self.generator._exprToSQL(df.limit)
        pre += lPre
        

        limitSQL = None
        if limitClause == "top":
          limitSQL = f"SELECT TOP {limitExpr} {df.alias}.* FROM ({parentSQL}) {df.alias}"
        elif limitClause == "limit":
          limitSQL = f"SELECT {df.alias}.* FROM ({parentSQL}) {df.alias} LIMIT {limitExpr}"
        else:
          raise ValueError(f"Unknown keyword for LIMIT: {limitClause}")

        if df.offset is not None:
          (oPre, offsetExpr) = self.generator._exprToSQL(df.offset)
          pre += oPre
          limitSQL += f" OFFSET {offsetExpr}"


        return (preCode+pre, limitSQL)
      
      elif isinstance(df, Ordering):
        subQry = Query(self.generator)
        (pre,parentSQL) = subQry._buildFrom(df.parents[0])

        by = []
        for attr in df.by:
          (exprPre, exprSQL) = self.generator._exprToSQL(attr)
          pre += exprPre
          by.append(exprSQL)

        by = ",".join(by)
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
    super().__init__()

  
  @staticmethod
  def _unindent(lines: List[str]) -> List[str]:
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

  def _exprToSQL(self, expr) -> Tuple[List[str], str]:
    exprSQL = ""
    pre = []

    # right hand side is a string constant
    if expr is None:
      exprSQL = "NULL"

    elif isinstance(expr,str):
      exprSQL = expr # TODO: currently to handle *, but maybe this should done earlier and be converted into a special ColRef?
    
    # we were given a constant
    elif isinstance(expr, Constant):
      if isinstance(expr.value, str):
        exprSQL = f"'{expr.value}'"
      elif isinstance(expr.value, list):
        
        eSQLs = []
        for x in expr.value:
          (ePre, eSQL) = self._exprToSQL(x)
          eSQLs.append(eSQL)
          pre += ePre

        exprSQL = ",".join(eSQLs)
        exprSQL = f"({exprSQL})"

      else:
        exprSQL = f"{expr.value}"

    # TODO: should LogicExpr be merged into BoolExpr ? 
    elif isinstance(expr, LogicExpr):

      (lPre,l) = self._exprToSQL(expr.left)
      (rPre,r) = self._exprToSQL(expr.right)

      if isinstance(expr.left, LogicExpr):
        l = f"({l})"
      if isinstance(expr.right, LogicExpr):
        r = f"({r})"

      if expr.operand == LogicOperation.AND:
        exprSQL = f"{l} and {r}"
      elif expr.operand == LogicOperation.OR:
        exprSQL = f"{l} or {r}"
      elif expr.operand == LogicOperation.NOT:
        exprSQL = f"not {l}"
      elif expr.operand == LogicOperation.XOR:
        exprSQL = f"{l} xor {r}"
      else:
        raise ExpressionException(f"unknown logical operation: {expr.operand}")

      pre = lPre + rPre

    elif isinstance(expr, BoolExpr):
      
      if not expr.right and not (expr.operand == BooleanOperation.EQ or expr.operand == BooleanOperation.NE):
        raise ExpressionException("only == and != allowed for comparison with None (NULL)")
          
      (lPre,l) = self._exprToSQL(expr.left)
      (rPre,r) = self._exprToSQL(expr.right)
        
      opStr = None
      if expr.operand == BooleanOperation.EQ:
        opStr = "=" if expr.right is not None else "is"
      elif expr.operand == BooleanOperation.NE:
        opStr = "<>" if expr.right is not None else "is not"
      elif expr.operand == BooleanOperation.GE:
        opStr = ">=" 
      elif expr.operand == BooleanOperation.GT:
        opStr = ">"
      elif expr.operand == BooleanOperation.LE:
        opStr = "<="
      elif expr.operand == BooleanOperation.LT:
        opStr = "<"
      else: 
        raise ExpressionException(f"unknown boolean operation: {expr.operand}")

      exprSQL = f"{l} {opStr} {r}"
      pre = lPre + rPre

    elif isinstance(expr, ArithmExpr):
      (lPre,l) = self._exprToSQL(expr.left)
      (rPre,r) = self._exprToSQL(expr.right)

      if not isinstance(expr.left, ColRef) and not isinstance(expr.left, Constant):
        l = f"({l})"
      if not isinstance(expr.right, ColRef) and not isinstance(expr.right, Constant):
        r = f"({r})"

      opStr = None
      if expr.operand == ArithmeticOperation.ADD:
        opStr = "+"
      elif expr.operand == ArithmeticOperation.SUB:
        opStr = "-"
      elif expr.operand == ArithmeticOperation.MUL:
        opStr = "*"
      elif expr.operand == ArithmeticOperation.DIV:
        opStr = "/"
      elif expr.operand == ArithmeticOperation.MOD:
        opStr = "%"
      
      exprSQL = f"{l} {opStr} {r}"
      pre = lPre + rPre

    elif isinstance(expr, SetExpr):
      (lPre,l) = self._exprToSQL(expr.left)

      if isinstance(expr.right, list):
        (rPre, r) = ([], ",".join([str(x) for x in expr.right]))
      else: # should be a DF
        (rPre,r) = self._exprToSQL(expr.right)

      if not isinstance(expr.left, ColRef) and not isinstance(expr.left, Constant):
        l = f"({l})"
      if not isinstance(expr.right, ColRef) and not isinstance(expr.right, Constant):
        r = f"({r})"

      opStr = "UNKNOWN"
      if expr.operand == SetOperation.IN:
        opStr = "IN"

      exprSQL = f"{l} {opStr} {r}"
      pre = lPre + rPre

    # if the thing to produce is a DataFrame, we probably have a subquery
    elif isinstance(expr, DataFrame): 
      # if right hand side is a DataFrame, we need to create code first 
      subQry = Query(self)
      (pre,exprSQL) = subQry._buildFrom(expr)
      

    # it's a plain column reference  
    elif isinstance(expr, ColRef):
      if expr.df and expr.column != "*":
        exprSQL = f"{expr.df.alias}.{expr.column}"
      else:
        exprSQL = expr.column

      if expr.alias:
        exprSQL += f" as {expr.alias}"

    # it's a computed column, the value could be anything
    elif isinstance(expr, ComputedCol):
      (pre, exprSQL) = self._exprToSQL(expr.value)

      if not isinstance(expr.value, FuncCall):
        exprSQL = f"({exprSQL})"

        if expr.alias:
          exprSQL = f"{exprSQL} as {expr.alias}"      

    # it's a function call -> produce CREATE func if necessary and call
    elif isinstance(expr, FuncCall):

      (pre,exprSQL) = self._generateFuncCall(expr)
      
    # seems to be something we forgot above or unknown to us. raise an exception  
    else:
      raise ExpressionException(f"don't know how to handle {expr}")

    return (pre,exprSQL)

  @staticmethod
  def _generateCreateFunc(udf: UDF, templates) -> str:
    paramsStr = ",".join([f"{p.name} {SQLGenerator._mapTypes(p.type)}" for p in udf.params])
    returnType = SQLGenerator._mapTypes(udf.returnType)

    if isinstance(udf, ModelUDF):
      lines = templates[udf.modelType.name + "_code"]
      for key, value in udf.templace_replacement_dict.items():
        lines = lines.replace(key, str(value))

    else:
      lines = udf.lines[1:]
      lines = SQLGenerator._unindent(lines)
      lines = "".join(lines)

    template = templates["createfunction"]
    code = template.replace("$$name$$", udf.name)\
      .replace("$$inparams$$",paramsStr)\
      .replace("$$returntype$$",returnType)\
      .replace("$$code$$",lines)
    return code

  @staticmethod
  def _getSQLFuncName(aggType) -> str:
    if isinstance(aggType, str):
      return aggType

    if isinstance(aggType, AggregateType):
      if aggType == AggregateType.MEAN:
        return "avg"

      return str(aggType)[len("AggregateType."):].lower()

    # if we get here it's not a string and not a AggType --> error
    raise ExpressionException(f"invalid function value: {aggType}, expected string or AggregateType, but got {type(aggType)}")

  def _generateFuncCall(self, f: FuncCall):
    if f.udf:
      pre = [SQLGenerator._generateCreateFunc(f.udf, self.templates)]
    else:
      pre = []

    cols = [] if len(f.inputCols) > 0 else ["*"]

    for col in f.inputCols:
      (p,c) = self._exprToSQL(col)
      pre += p
      cols.append(c)

    inCols = ",".join(cols)

    fName = SQLGenerator._getSQLFuncName(f.funcName)

    funcCode = f"{fName}({inCols})"

    if f.alias:
      funcCode += f" as {f.alias}"

    return (pre,funcCode)

  @staticmethod
  def _generateCreateExtTable(tab: ExternalTable, templates) -> List[str]:
    queries = []

    # In place string replacement
    for i in range(len(tab.colDefs)):
      tab.colDefs[i] = tab.colDefs[i].replace(":", " ").replace("str", "VARCHAR(1024)")
    schemaString = ",".join(tab.colDefs)

    vectoroptions = [f"'delimiter'='{tab.delimiter}'"]
    if not tab.hasHeader:
      vectoroptions.append("'header'='false'")
      vectoroptions.append(f"'schema'='{schemaString}'")
    vectoroptionString = f""", OPTIONS=({",".join(vectoroptions)})"""

    postgresoptions = f"filename '{tab.filenames}', format '{tab.format}', delimiter '{tab.delimiter}'"

    template = templates["externaltable"]
    assert isinstance(template, list), "External table template must be a list"
    
    for t in template:
      code = t.replace("$$name$$", tab.table)\
        .replace("$$schema$$", schemaString)\
        .replace("$$filenames$$", tab.filenames)\
        .replace("$$format$$", tab.format)\
        .replace("$$vectoroptions$$", vectoroptionString)\
        .replace("$$postgresoptions$$", postgresoptions)\
        .replace("$$fdw_extension_name$$", tab.fdw_extension_name)
      queries.append(code)
    
    return queries

  
  def _generateAggCode(self, df, f) -> Tuple[List[str],str]:
    # aggregation over a table is performed in a way that the actual query
    # that was built is executed as an inner query and around that, we 
    # compute the aggregation
    (pre, innerSQL) = self.generate(df)
    if df.parents:
      df.alias = GrizzlyGenerator._incrAndGetTupleVar()
      (fPre,funcCode) = self._generateFuncCall(f)
      aggSQL = f"SELECT {funcCode} FROM ({innerSQL}) as {df.alias}"
      
    else:
      (fPre,funcCode) = self._generateFuncCall(f)
      aggSQL = f"SELECT {funcCode} FROM {df.table} {df.alias}"

    return (pre+fPre, aggSQL)

  def generate(self, df) -> Tuple[List[str],str]:
    qry = Query(self)
    (preQueryCode, qryString) = qry._buildFrom(df)

    return (preQueryCode, qryString)
