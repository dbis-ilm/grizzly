from grizzly.dataframes.schema import ColType
from grizzly.config import Config
from grizzly.aggregates import AggregateType
from grizzly.dataframes.frame import Limit, Ordering, UDF, ModelUDF, Table, ExternalTable, Projection, Filter, Join, Grouping, DataFrame, Union
from grizzly.expression import AllColumns, ArithmExpr, ArithmeticOperation, BoolExpr, BooleanOperation, ComputedCol, Constant, ExpressionException, FuncCall, ColRef, LogicExpr, LogicOperation, SetExpr, SetOperation
from grizzly.generator import GrizzlyGenerator

import grizzly.udfcompiler as udfcompiler
from grizzly.udfcompiler.udfcompiler_exceptions import UDFCompilerException

from typing import List, Set, Tuple
import re
import logging
logger = logging.getLogger(__name__)

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
      line = line[numLeadingSpaces:]
      if line.strip() == "":
        line = "\n"
      resultLines.append(line)

    return resultLines

  @staticmethod
  def _mapTypes(pythonType: str, mapping) -> str:
    if pythonType in mapping:
      remove_parenthesis = mapping['remove_parenthesis'] if 'remove_parenthesis' in mapping else False
      if remove_parenthesis:
        remove_parenthesis_expr = "[\(].*?[\)]"
        return re.sub(remove_parenthesis_expr, "", mapping[pythonType])
      return mapping[pythonType]
    
    return pythonType

  @staticmethod
  def _mapFromSQLTypes(sqlType: str):
    if sqlType is None:
      return ColType.UNKNOWN

    sqlType = sqlType.strip().lower()

    if sqlType.startswith("int") or sqlType == "bigint" or sqlType.startswith("float") or sqlType.startswith("double") or sqlType.startswith("tiny"):
      return ColType.NUMERIC
    
    elif sqlType.startswith("varchar") or sqlType.startswith("char") or sqlType.startswith("text"):
      return ColType.TEXT

    elif sqlType.startswith("bool"):
      return ColType.BOOL

    else:
      return ColType.UNKNOWN

  def _exprToSQL(self, expr) -> Tuple[List[str], str]:
    exprSQL = ""
    pre = []

    # right hand side is a string constant
    if expr is None:
      exprSQL = "NULL"

    elif isinstance(expr,str):
      raise ValueError(f"string is not an expresion! {expr}")
      
      # exprSQL = expr # TODO: currently to handle *, but maybe this should done earlier and be converted into a special ColRef?
    
    # we were given a constant
    elif isinstance(expr, Constant):
      alias = f"as {expr.alias}" if expr.alias is not None else ""
      if isinstance(expr.value, str):
        exprSQL = f"'{expr.value}' {alias}"
      elif isinstance(expr.value, list):
        
        eSQLs = []
        for x in expr.value:
          (ePre, eSQL) = self._exprToSQL(x)
          eSQLs.append(eSQL)
          pre += ePre

        exprSQL = ",".join(eSQLs)
        exprSQL = f"({exprSQL})"

      else:
        exprSQL = f"{expr.value} {alias}"

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

    elif isinstance(expr, SetExpr): # must be handled before BoolExpr
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

    

    # if the thing to produce is a DataFrame, we probably have a subquery
    elif isinstance(expr, DataFrame): 
      # if right hand side is a DataFrame, we need to create code first 
      (pre,exprSQL) = self._buildFrom(expr)
      
    elif isinstance(expr, AllColumns): # must be checked befor ColRef!
      exprSQL = "*"

    # it's a plain column reference  
    elif isinstance(expr, ColRef):

      if expr.df is not None:
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

        if expr.alias is not None and expr.alias != "":
          exprSQL = f"{exprSQL} as {expr.alias}"      

    # it's a function call -> produce CREATE func if necessary and call
    elif isinstance(expr, FuncCall):

      (pre,exprSQL) = self._generateFuncCall(expr)
      
    elif isinstance(expr, tuple) or isinstance(expr, list):
      sqls = []
      for i in expr:
        (exprPre,sql) = self._exprToSQL(i)
        pre  += exprPre
        sqls.append(sql)

      sqls = "(" + ",".join([str(s) for s in sqls]) + ")"

      exprSQL = sqls  


    # seems to be something we forgot above or unknown to us. raise an exception  
    else:
      raise ExpressionException(f"don't know how to handle {expr}")

    return (pre,exprSQL)

  def _buildFrom(self,df): #-> Tuple[List[str], str, str]:

    if df is not None:

      computedCols = []
      preCode = []

      for x in df.computedCols:
        (exprPre, exprSQL) = self._exprToSQL(x)
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

        tablePre = SQLGenerator._generateCreateExtTable(df, self.templates)
        qry = f"SELECT {proj} FROM {df.table} {df.alias}"

        return (preCode + tablePre, qry)

      elif isinstance(df,Projection):
        (pre,parentSQL) = self._buildFrom(df.parents[0])

        prefixed = "*"
        if df.columns:
          prefixed = []

          for attr in df.columns:
            (ePre, exprSQL) = self._exprToSQL(attr)

            pre += ePre
            prefixed.append(exprSQL)
          
          prefixed = ",".join(prefixed)

        if computedCols:
          prefixed += ","+computedCols

        qry = f"SELECT { 'DISTINCT ' if df.doDistinct else ''}{prefixed} FROM ({parentSQL}) {df.alias}"
        
        return (preCode + pre, qry)

      elif isinstance(df,Filter):
        (pre,parentSQL) = self._buildFrom(df.parents[0])

        (exprPre,exprStr) = self._exprToSQL(df.expr)

        proj = "*"
        if computedCols:
          proj += ","+computedCols

        qry = f"SELECT {proj} FROM ({parentSQL}) {df.alias} WHERE {exprStr}"

        return (preCode + pre + exprPre, qry)

      elif isinstance(df, Join):

        (lpre,lparentSQL) = self._buildFrom(df.leftParent())

        (rpre,rparentSQL) = self._buildFrom(df.rightParent())

        lAlias = df.leftParent().alias
        rAlias = df.rightParent().alias

        if isinstance(df.on, ColRef):
          (exprPre, onSQL) = self._exprToSQL(df.on)
          onSQL = f"USING ({onSQL})"
          preCode += exprPre
        elif isinstance(df.on, LogicExpr) or isinstance(df.on, BoolExpr):
          (exprPre, onSQL) = self._exprToSQL(df.on)
          onSQL = "ON " + onSQL
          preCode += exprPre
        elif isinstance(df.on, list):

          if len(df.on) != 2:
            raise ExpressionException("on condition must consist of exacltly two columns")

          (lOnPre,lOn) = self._exprToSQL(df.on[0])
          (rOnPre,rOn) = self._exprToSQL(df.on[1])

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

      elif isinstance(df, Union):
        (lpre,lparentSQL) = self._buildFrom(df.leftParent())

        (rpre,rparentSQL) = self._buildFrom(df.rightParent())

        allKW = "ALL" if not df.distinct else ""

        unionSQL = f"{lparentSQL} UNION {allKW} {rparentSQL}"

        return (preCode + lpre + rpre, unionSQL)

      elif isinstance(df, Grouping):
        (pre,parentSQL) = self._buildFrom(df.parents[0])

        byCols = []
        for attr in df.groupCols:
          (exprPre, exprSQL) = self._exprToSQL(attr)
          pre += exprPre
          byCols.append(exprSQL)

        by = ",".join(byCols)

        funcCode = ""
        for f in df.aggFunc:
          (fPre,fCode) = self._generateFuncCall(f)
          pre += fPre
          funcCode += ", " + fCode
        
        groupSQL = f"SELECT {by} {funcCode} FROM ({parentSQL}) {df.alias} GROUP BY {by}"

        havings = []
        if df.having:
          for h in df.having:
            (hPre,hSQL) = self._exprToSQL(h)
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
        (pre,parentSQL) = self._buildFrom(df.parents[0])

        limitClause = self.templates["limit"].lower()

        (lPre,limitExpr) = self._exprToSQL(df.limit)
        pre += lPre
        

        limitSQL = None
        if limitClause == "top":
          limitSQL = f"SELECT TOP {limitExpr} {df.alias}.* FROM ({parentSQL}) {df.alias}"
        elif limitClause == "limit":
          limitSQL = f"SELECT {df.alias}.* FROM ({parentSQL}) {df.alias} LIMIT {limitExpr}"
        else:
          raise ValueError(f"Unknown keyword for LIMIT: {limitClause}")

        if df.offset is not None:
          (oPre, offsetExpr) = self._exprToSQL(df.offset)
          pre += oPre
          limitSQL += f" OFFSET {offsetExpr}"


        return (preCode+pre, limitSQL)
      
      elif isinstance(df, Ordering):
        (pre,parentSQL) = self._buildFrom(df.parents[0])

        by = []
        for attr in df.by:
          (exprPre, exprSQL) = self._exprToSQL(attr)
          pre += exprPre
          by.append(exprSQL)

        direction = ""
        # If ascending is not specified, default is ascending on all columns. If specifiec, it can 
        # be a bool for the order on all columns or a list, specifying a columnwise order.
        if df.ascending is not None:
          if isinstance(df.ascending, list):
            by = [i + " " + ("ASC" if j else "DESC") for i, j in zip(by, df.ascending)]
          else:
            direction = "ASC" if df.ascending else "DESC"
        else:
          direction = "ASC"

        by = ",".join(by)

        qry = f"SELECT * FROM ({parentSQL}) {df.alias} ORDER BY {by} {direction}"

        return (preCode+pre, qry)

      else:
        raise ValueError(f"unsupported operator {type(df)}")

    else:
      return ("","")


  @staticmethod
  def _generateCreateFunc(udf: UDF, templates) -> str:
    isVectorizedFunction = udf.name.startswith("vec_")

    vectorsArePassed = templates["vectorized_udfs"] if "vectorized_udfs" in templates else False
    template = templates[f"createfunction_{udf.lang}"]

    paramsStr = ""

    if not isinstance(udf, ModelUDF):
      # remove signature
      signature = udf.lines[0]
      lines = udf.lines[1:]

    # e.g. MonetDB passes vectors to UDF. If the user expects scalar values we have to wrap it manually but maintain variable names!
    if vectorsArePassed and not isVectorizedFunction: 
      paramNames = [f"_{p.name}" for p in udf.params ] # input param names
      paramNamesStr = ",".join(paramNames)
      paramsStr = ",".join([f"{n} {SQLGenerator._mapTypes(p.type, templates['types'])}" for (n, p) in zip(paramNames, udf.params)]) # param declaration in signature
      varNames = [f"{p.name}" for p in udf.params ] # var names to use in loop
      varNamesStr = ",".join(varNames)

      lines = [signature.replace(udf.name, "_"+udf.name)] + lines

      loop = ""

      if len(udf.params) > 1:
        # loop = f"for ({varNamesStr}) in zip({paramNamesStr}):\n"
        loop = f"return [ _{udf.name}({varNamesStr}) for ({varNamesStr}) in zip({paramNamesStr}) ]\n"
      else:
        loop = f"return [ _{udf.name}({varNamesStr}) for {varNamesStr} in {paramNamesStr} ]\n"

      lines.append(loop)
    else:
      paramsStr = ",".join([f"{p.name} {SQLGenerator._mapTypes(p.type, templates['types'])}" for p in udf.params])

    returnType = SQLGenerator._mapTypes(udf.returnType, templates['types'])
    
    leadingSpaces = 0
    for line in template.split("\n"):
      if "$$code$$" in line:
        # leadingSpaces = line.find("$$code$$")
        leadingSpaces = len(line) - len(line.lstrip())
        break

    pre = ""
    if isinstance(udf, ModelUDF):
      lines = templates[udf.modelType.name + "_code"]
      for key, value in udf.templace_replacement_dict.items():
        lines = lines.replace(key, str(value))

    else:
      
      # lines = udf.lines
      lines = SQLGenerator._unindent(lines) # unindent, depends on where in the script the function was defined

      lines = [" "*leadingSpaces + line for line in lines] 

      lines = "".join(lines) # put back together

      if udf.lang == "sql":
        try:
          # Try to compile code of udf and pass mapping template
          pre, lines = udfcompiler.compile(lines, templates, udf.params)
        except Exception as e:
          logger.info(f'Compiling of UDF to "{udf.lang}" failed: {e}')
          # If compiling fails try fallbackmode with PL/PY translation if wanted
          if udf.fallback == True:
            try:
              # Load Function creation template with python code
              template = templates["createfunction_py"]
              logger.info('Fallback to UDF execution with PL/Python...')
            except ValueError:
              logger.info('Fallback to UDF execution with PL/Python failed')
              # Raise exception to make Fallback with pandas possible
              raise UDFCompilerException(f'Compiling of UDF "{udf.name}" to "{udf.lang}" failed')
          else:
            raise

    # print(lines)

    code = template.replace("$$name$$", udf.name)\
      .replace("$$pre$$", pre)\
      .replace("$$inparams$$",paramsStr)\
      .replace("$$returntype$$",returnType)\
      .replace("$$code$$",lines)\
      .replace("//", "\n")

    return code

  @staticmethod
  def _getSQLFuncName(aggType) -> str:
    if isinstance(aggType, str):
      return aggType

    if isinstance(aggType, AggregateType):
      if aggType == AggregateType.MEAN:
        return "avg"

      return AggregateType.getName(aggType)

    # if we get here it's not a string and not a AggType --> error
    raise ExpressionException(f"invalid function value: {aggType}, expected string or AggregateType, but got {type(aggType)}")

  def _generateFuncCall(self, f: FuncCall):
    if f.udf:
      pre = [SQLGenerator._generateCreateFunc(f.udf, self.templates)]
    else:
      pre = []

    if f.inputCols:
      cols = []

      for col in f.inputCols:
        (p,c) = self._exprToSQL(col)
        pre += p
        cols.append(c)

      inCols = ",".join(cols)
    else:
      inCols = ""

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

    monetdboffset = 1 if tab.hasHeader == False else 2

    template = templates["externaltable"]
    assert isinstance(template, list), "External table template must be a list"
    
    for t in template:
      code = t.replace("$$name$$", tab.table)\
        .replace("$$schema$$", schemaString)\
        .replace("$$filenames$$", tab.filenames)\
        .replace("$$format$$", tab.format)\
        .replace("$$vectoroptions$$", vectoroptionString)\
        .replace("$$postgresoptions$$", postgresoptions)\
        .replace("$$monetdboffset$$", str(monetdboffset))\
        .replace("$$fdw_extension_name$$", tab.fdw_extension_name)
      queries.append(code)
    
    return queries

  
  def _generateAggCode(self, df, f) -> Tuple[Set[str],str]:
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

    preQuery = SQLGenerator._makeUnique(pre + fPre)

    return (preQuery, aggSQL)

  def generate(self, df) -> Tuple[Set[str],str]:
    (preQueryCode, qryString) = self._buildFrom(df)

    preQueryCode = SQLGenerator._makeUnique(preQueryCode)

    return (preQueryCode, qryString)

  def getTableSchema(self, tableName):
    
    qry = None
    columnNames = None
    columnTypes = None
    if "schema_query" in self.templates: 
      qry = self.templates["schema_query"]
      qry = qry.replace("$$tablename$$",tableName)
      columnNames = self.templates["colname_column"]
      columnTypes = self.templates["coltype_column"]
    elif "schema_table" in self.templates:
      schematable = self.templates["schema_table"]
      tablenameCol = self.templates["tablename_column"]
      colname_column = self.templates["colname_column"]
      coltype_column = self.templates["coltype_column"]
      qry = f"SELECT {colname_column}, {coltype_column} FROM {schematable} where {tablenameCol} = '{tableName}'"
      columnNames = 0
      columnTypes = 1

    return (qry, columnNames, columnTypes)


  @staticmethod
  def _makeUnique(preQueries: List[str]) -> List[str]:

    result = []
    hashes = set()

    if isinstance(preQueries, str):
      return [preQueries]

    for pq in preQueries:
      h = hash(pq)
      if h not in hashes:
        result.append(pq)
        hashes.add(h)

    return result
