from .sqlops import From, Filter, Projection, Grouping, Join
from .column import Expr, Eq, Ne, Gt, Ge, Lt, Le, And, Or
from .query import Query
from .connection import Connection

# from beautifultable import BeautifulTable

class DataFrameOld(object):

  def __init__(self, columns, parents):
    self.columns = columns
    self.parents = parents


  

#####################################################
### aggregates

  


  def _execAgg(self, func, col):
    """
    Actually compute the aggregation function.

    If we have a GROUP BY operation, the aggregation is only stored
    as a transformation and needs to be executed using show() or similar.

    If no grouping exists, we want to compute the aggregate over the complete
    table and return the scalar result directly
    """
    colName = None
    if col is None:
      colName = self.columns[0]
    else:
      colName = col

    funcCode = f"{func}({colName})"  

    if isinstance(self.op, Grouping):
      newOp = Grouping(self.op.groupcols, self.op.parent)
      newOp.setAggFunc(funcCode)
      
      return DataFrame(self.columns, newOp)
      
    else:
      return self._doExecAgg(funcCode)
    

  def _doExecAgg(self, funcCode):
    """
    Really executes the aggregation and returns the single result
    """

    # aggregation over a table is performed in a way that the actual query
    # that was built is executed as an inner query and around that, we 
    # compute the aggregation
    innerSQL = self.sql()
    aggSQL = f"SELECT {funcCode} FROM ({innerSQL}) as t"
    
    # execute an SQL query and get the result set
    rs = self._doExecQuery(aggSQL)
    #fetch first (and only) row, return first column only
    return rs.fetchone()[0]


  def _doExecQuery(self, qry):
    """
    Execute an arbitrary SQL query and return the result set
    """
    cursor = Connection.db.cursor()
    cursor.execute(qry)
    return cursor

### produce SQL string
  def sql(self):
    """
    Produce a SQL string from the current operator tree
    """

    # the query object
    qry = Query()

    # traverse the "query plan" and fill the query object
    currOp = self.op
    while currOp != None:
      
      if isinstance(currOp, Filter):
        qry.filters.append(currOp)
      elif isinstance(currOp, Projection):
        qry.projList = currOp.attrs
        if currOp.distinct:
          qry.distinct = "distinct"
      elif isinstance(currOp, From):
        qry.froms= currOp.relation
      elif isinstance(currOp, Grouping):
        fqn = map(lambda x: f"{currOp.name()}.{x}", currOp.groupcols)
        qry.groupcols.extend(fqn)
        qry.groupagg = currOp.aggFunc
      elif isinstance(currOp, Join):
        qry.joins.append(currOp)

      currOp = currOp.parent

    # let the query object produce the actual SQL
    return qry.sql()

### Run query and print results
  def show(self, delim = ",",pretty=False, maxColWidth=20):
    """
    Execute the operations and print results to stdout

    Non-pretty mode outputs in CSV style -- the delim parameter can be used to 
    set the delimiter. Non-pretty mode ignores the maxColWidth parameter.
    """

    rs = self._doExecQuery(self.sql())
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

  def __str__(self):
    from beautifultable import BeautifulTable

    table = BeautifulTable()

    rs = self._doExecQuery(self.sql())
  
    for row in rs:
      table.append_row(row)


    rs.close()

    return str(table)