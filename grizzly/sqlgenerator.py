import random
import string

from grizzly.dataframes.frame import Table, Projection, Filter, Join, Grouping, DataFrame
from grizzly.expression import ColRef, Expr
from grizzly.aggregates import AggregateType
from grizzly.generator import GrizzlyGenerator

class Query:

  def __init__(self):
    self.filters = []
    self.projections = None
    self.doDistinct = False
    self.table = None
    self.groupcols = []
    self.groupagg = None
    self.joins = []

  def _reset(self):
    self.filters = []
    self.projections = None
    self.doDistinct = False
    self.table = None
    self.groupcols = []
    self.groupagg = None
    self.joins = []

  def _doExprToSQL(self, expr):
    exprSQL = ""
    # right hand side is a string constant
    if isinstance(expr, str):
      exprSQL = f"'{expr}'"
    # right hand side is a dataframe (i.e. subquery)
    elif isinstance(expr, DataFrame): 
      # if right hand side is a DataFrame, we need to create code first 
      subQry = Query()
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

    curr = df
    while curr is not None:

      if isinstance(curr,Table):
        self.table = f"{curr.table} {curr.alias}"

      elif isinstance(curr,Projection):
        if curr.attrs:
          prefixed = [str(attr) for attr in curr.attrs]
          if not self.projections:
            self.projections = prefixed
          else:
            set(self.projections).intersection(set(prefixed))
        

        if curr.doDistinct:
          self.doDistinct = True

      elif isinstance(curr,Filter):
        exprStr = self._exprToSQL(curr.expr)
        self.filters.append(exprStr)

      elif isinstance(curr, Join):
        # rtVar = DataFrame._incrAndGetTupleVar()
        

        if isinstance(curr.right, Table):
          rightSQL = curr.right.table
          rtVar = curr.right.alias
        else:
          subQry = Query()
          rightSQL = f"({subQry._buildFrom(curr.right)})"
          rtVar = GrizzlyGenerator._incrAndGetTupleVar()
          # curr.right.alias = rtVar
          curr.right.setAlias(rtVar)

        if isinstance(curr.on, Expr):
          onSQL = self._exprToSQL(curr.on)
        else:
          onSQL = f"{curr.alias}.{curr.on[0]} {curr.comp} {rtVar}.{curr.on[1]}"
        
        joinSQL = f"{curr.how} JOIN {rightSQL} {rtVar} ON {onSQL}"
        self.joins.append(joinSQL)

      elif isinstance(curr, Grouping):
        self.groupcols = [str(attr) for attr in curr.groupCols]

      if curr.parents is None:
        curr = None
      else:
        curr = curr.parents[0]

    joins = ""
    while self.joins:
      joins += " "+self.joins.pop()
    
    projs = "*"
    if self.projections:
      if self.groupcols and not self.projections.issubset(self.groupcols):
        raise ValueError("Projection list must be subset of group columns")

      projs = ', '.join(self.projections)

    grouping = ""
    if self.groupcols:
      theColRefs = ", ".join([str(e) for e in self.groupcols])
      grouping += f" GROUP BY {theColRefs}"

      if projs == "*":
        projs = theColRefs

    if self.doDistinct:
      projs = "distinct " + projs

    where = ""
    if len(self.filters) > 0:
      exprs = " AND ".join([str(e) for e in self.filters])
      where += f" WHERE {exprs}"

    qrySoFar = f"SELECT {projs} FROM {self.table}{joins}{where}{grouping}"
    return qrySoFar

class SQLGenerator:

  def __init__(self, executor):
    self.executor = executor

  def close(self):
    self.executor.close()

  def generate(self, df):
    qry = Query()
    return qry._buildFrom(df)

  def toString(self, df):
    from beautifultable import BeautifulTable

    table = BeautifulTable()

    sql = self.generate(df)
    rs = self.executor.execute(sql)
  
    for row in rs:
      table.append_row(row)

    rs.close()

    return str(table)

  def execute(self, df, delim = ",",pretty=False, maxColWidth=20):
    """
    Execute the operations and print results to stdout

    Non-pretty mode outputs in CSV style -- the delim parameter can be used to 
    set the delimiter. Non-pretty mode ignores the maxColWidth parameter.
    """

    sql = self.generate(df)
    rs = self.executor.execute(sql)
    cols = [dec[0] for dec in rs.description]
    

    if not pretty:
      print(delim.join(cols))
      for row in rs:
        print(delim.join([str(col) for col in row]))
    else:
      firstRow = rs.fetchone()

      colWidths = [ min(maxColWidth, max(len(x),len(str(y)))) for x,y in zip(cols, firstRow)]

      rowFormat = "|".join([ "{:^"+str(width+2)+"}" for width in colWidths])
      

      # print(rowFormat.format(*cols))
      def printRow(theRow):
        values = []
        for col, colWidth in zip(theRow, colWidths):
          strCol = str(col)
          if len(strCol) > colWidth:
            values.append(strCol[:(colWidth-3)]+"...")
          else:
            values.append(strCol)

        print(rowFormat.format(*values))

      printRow(cols)
      printRow(firstRow)
      for row in rs:
        printRow(row)

    rs.close()


  def _execAgg(self, df, col, func):
    """
    Actually compute the aggregation function.

    If we have a GROUP BY operation, the aggregation is only stored
    as a transformation and needs to be executed using show() or similar.

    If no grouping exists, we want to compute the aggregate over the complete
    table and return the scalar result directly
    """
    # colName = None
    # if col is None:
    #   colName = self.columns[0]
    # else:
    #   colName = col
    colName = col
    
    if func == AggregateType.MEAN:
      funcStr = "avg"
    else:
      funcStr = str(func).lower()[len("aggregatetype."):]

    funcCode = f"{funcStr}({colName})"  

    # if isinstance(df, Grouping):
    #   newOp = Grouping(self.op.groupcols, self.op.parent)
    #   newOp.setAggFunc(funcCode)
      
    #   return DataFrame(self.columns, newOp)
      
    # else:
    return self._doExecAgg(funcCode, df)

  def _doExecAgg(self, funcCode, df):
    """
    Really executes the aggregation and returns the single result
    """

    # aggregation over a table is performed in a way that the actual query
    # that was built is executed as an inner query and around that, we 
    # compute the aggregation
    if df.parents:
      innerSQL = self.generate(df.parents[0])
      aggSQL = f"SELECT {funcCode} FROM ({innerSQL}) as t"
    else:
      aggSQL = f"SELECT {funcCode} FROM {df.table}"
    
    # execute an SQL query and get the result set
    rs = self.executor.execute(aggSQL)
    #fetch first (and only) row, return first column only
    return rs.fetchone()[0]