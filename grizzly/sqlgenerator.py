from grizzly.aggregates import AggregateType
from grizzly.dataframes.frame import UDF, Table, ExternalTable, Projection, Filter, Join, Grouping, DataFrame
from grizzly.expression import FuncCall, ColRef, Expr
from typing import List
from grizzly.generator import GrizzlyGenerator

import random
import string

class Query:

  def __init__(self, generator):
    self.generator = generator

    self.filters = []
    self.projections = None
    self.doDistinct = False
    self.table = None
    self.groupcols = []
    self.groupagg = set()
    self.joins = []
    self.preQueryCode = []

  def _reset(self):
    self.filters = []
    self.projections = None
    self.doDistinct = False
    self.table = None
    self.groupcols = []
    self.groupagg = set()
    self.joins = []
    self.preQueryCode = []

  def _doExprToSQL(self, expr):
    exprSQL = ""
    # right hand side is a string constant
    if isinstance(expr, str):
      exprSQL = f"'{expr}'"
    # right hand side is a dataframe (i.e. subquery)
    elif isinstance(expr, DataFrame): 
      # if right hand side is a DataFrame, we need to create code first 
      subQry = Query(self.generator)
      exprSQL = subQry._buildFrom(expr)

    elif isinstance(expr, ColRef):
      exprSQL = str(expr)

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

  def _buildFrom(self,df):

    computedCols = []

    curr = df
    while curr is not None:

      computedCols += curr.computedCols        

      if isinstance(curr,Table):
        self.table = f"{curr.table} {curr.alias}"

      elif isinstance(curr, ExternalTable):
        self.table = f"{curr.table} {curr.alias}"
        self.preQueryCode.extend(SQLGenerator._generateCreateExtTable(curr))

      elif isinstance(curr,Projection):
        if curr.attrs:
          prefixed = [str(attr) for attr in curr.attrs]
          if not self.projections:
            self.projections = prefixed
          else:
            # FIXME: does this work? no return, no assignment
            set(self.projections).intersection(set(prefixed))
        

        if curr.doDistinct:
          self.doDistinct = True

      elif isinstance(curr,Filter):
        exprStr = self._exprToSQL(curr.expr)
        self.filters.append(exprStr)

      elif isinstance(curr, Join):

        if isinstance(curr.right, Table):
          rightSQL = curr.right.table
          rtVar = curr.right.alias
        else:
          subQry = Query(self.generator)
          rightSQL = f"({subQry._buildFrom(curr.right)})"
          rtVar = GrizzlyGenerator._incrAndGetTupleVar()
          # curr.right.alias = rtVar
          curr.right.setAlias(rtVar)

        if isinstance(curr.on, Expr):
          onSQL = "ON " + self._exprToSQL(curr.on)
        elif isinstance(curr.on, list):
          onSQL = f"ON {curr.alias}.{curr.on[0]} {curr.comp} {rtVar}.{curr.on[1]}"
        else:
          onSQL = ""

        joinSQL = f"{curr.how} JOIN {rightSQL} {rtVar} {onSQL}"
        self.joins.append(joinSQL)

      elif isinstance(curr, Grouping):
        self.groupcols = [str(attr) for attr in curr.groupCols]

        if curr.aggFunc:
          (func, col) = curr.aggFunc
          funcCode = SQLGenerator._getFuncCode(curr, col, func) 
          self.groupagg.add(funcCode)

      if curr.parents is None:
        curr = None
      else:
        curr = curr.parents[0]

    joins = ""
    while self.joins:
      joins += " "+self.joins.pop()
    
    projs = "*"
    if self.projections:
      if self.groupcols and not set(self.projections).issubset(self.groupcols):
        raise ValueError("Projection list must be subset of group columns")

      projs = ', '.join(self.projections) 

    if computedCols:
      computedStr = ", ".join([str(c) for c in computedCols])
      # TODO: this is not really correct if after the map we apply a projection to only this
      # computed attribute
      projs += ", "+computedStr

      self.preQueryCode += [ self.generator.generateCreateFunc(func.udf) for func in computedCols if isinstance(func, FuncCall) ]

    grouping = ""
    if self.groupcols:
      theColRefs = ", ".join([str(e) for e in self.groupcols])
      grouping += f" GROUP BY {theColRefs}"

      if projs == "*":
        projs = theColRefs

    if len(self.groupagg) > 0:
      if projs == "*":
        projs = self.groupagg
      elif len(self.groupagg) > 0:
        projs = projs + "," + ",".join(self.groupagg)

    if self.doDistinct:
      projs = "distinct " + projs

    where = ""
    if len(self.filters) > 0:
      exprs = " AND ".join([str(e) for e in self.filters])
      where += f" WHERE {exprs}"

    qrySoFar = f"SELECT {projs} FROM {self.table}{joins}{where}{grouping}"
    return qrySoFar

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


class SQLGenerator:

  def __init__(self, profile: str = None):
    self.profile = profile
    self.templates = Config.loadProfile(profile)
  
  def generateCreateFunc(self, udf: UDF) -> str:
    paramsStr = ",".join([f"{p.name} {p.type}" for p in udf.params])

    if udf.lines:
      lines = "".join(udf.lines)
    else:
      lines = self.templates["applymodelfunction"]

    template = self.templates["createfunction"]

    code = template.replace("$$name$$", udf.name).replace("$$inparams$$",paramsStr).replace("$$returntype$$",udf.returnType).replace("$$code$$",lines)

    return code

  @staticmethod
  def _generateCreateExtTable(tab: ExternalTable) -> List[str]:
    queries = []
    # In place string replacement
    for i in range(len(tab.colDefs)):
      tab.colDefs[i] = tab.colDefs[i].replace(":", " ").replace("str", "VARCHAR(1024)")
    schemaString = ",".join(tab.colDefs)

    queries.append(f"DROP TABLE IF EXISTS {tab.table}")

    code = f"CREATE EXTERNAL TABLE {tab.table}({schemaString}) USING SPARK WITH REFERENCE='{tab.filenames}'"

    if tab.format != "":
        code += f", FORMAT='{tab.format}'"

    options = [f"'delimiter'='{tab.delimiter}'"]
    if not tab.hasHeader:
      options.append("'header'='false'")
      options.append(f"'schema'='{schemaString}'")

    optionString = ",".join(options)
    code += f", OPTIONS=({optionString})"
    code += ";"
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

  def _generateAggCode(self, df, col, func):
    # aggregation over a table is performed in a way that the actual query
    # that was built is executed as an inner query and around that, we 
    # compute the aggregation

    if df.parents:
      (pre, innerSQL) = self.generate(df)
      df.alias = GrizzlyGenerator._incrAndGetTupleVar()
      funcCode = SQLGenerator._getFuncCode(df, col, func)
      prequeries = ";".join(pre)
      aggSQL = f"{prequeries};SELECT {funcCode} FROM ({innerSQL}) as {df.alias}"
      # aggSQL = innerSQL
    else:
      funcCode = SQLGenerator._getFuncCode(df, col, func)
      aggSQL = f"SELECT {funcCode} FROM {df.table} {df.alias}"

    return aggSQL

  def generate(self, df) -> (List[str],str):
    qry = Query(self)
    qryString = qry._buildFrom(df)

    return (qry.preQueryCode, qryString)