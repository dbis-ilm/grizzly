from grizzly.expression import ColRef
from grizzly.sqlgenerator import SQLGenerator
from grizzly.generator import GrizzlyGenerator

import logging

logger = logging.getLogger(__name__)

class RelationalExecutor(object):
  
  def __init__(self, connection, queryGenerator=SQLGenerator()):
    super().__init__()
    self.connection = connection
    self.queryGenerator = queryGenerator

  def generate(self, df):
    return self.queryGenerator.generate(df)

  def generateQuery(self, df):
    (pre,qry) = self.generate(df)
    prequeries = ";".join(pre)
    return f"{prequeries} {qry}"

  def _execute(self, sql):
    logger.debug(sql)
    cursor = self.connection.cursor()
    try:
      cursor.execute(sql)
      return cursor  
    except Exception as e:
      logger.error(f"Failed to execute query. Reason: {e}")
      logger.error(f"Query: {sql}")
      logger.exception(e)
      raise e
    

  def close(self):
    self.connection.close()

  def collect(self, df, includeHeader):
    rs = self.execute(df)

    tuples = []

    if includeHeader:
      cols = [dec[0] for dec in rs.description]
      tuples.append(cols)

    for row in rs:
      tuples.append(row)

    return tuples


  def table(self,df):
    rs = self.execute(df)
    import beautifultable
    table = beautifultable.BeautifulTable()
    for row in rs:
      table.rows.append(row)

    rs.close()
    return str(table)

  def toString(self, df, delim=",", pretty=False, maxColWidth=20, limit=20):
    rs = self.execute(df)

    if rs.description:
      cols = [dec[0] for dec in rs.description]
    else:
      cols = []

    if not pretty:
      strings = [delim.join(cols)]
      cnt = 0
      for row in rs:
        cnt += 1
        if limit is None or cnt <= limit:
          strings.append(delim.join([str(col) for col in row]))
        

      rs.close()

      if  limit is not None and cnt > limit and cnt - limit > 0:
        strings.append(f"and {cnt - limit} more...")

      return "\n".join(strings)
    else:
      firstRow = rs.fetchone()

      colWidths = [ min(maxColWidth, max(len(x),len(str(y)))) for x,y in zip(cols, firstRow)]

      rowFormat = "|".join([ "{:^"+str(width+2)+"}" for width in colWidths])
      

      def formatRow(theRow):
        values = []
        for col, colWidth in zip(theRow, colWidths):
          strCol = str(col)
          if len(strCol) > colWidth:
            values.append(strCol[:(colWidth-3)]+"...")
          else:
            values.append(strCol)

        return rowFormat.format(*values)

      resultRep = [formatRow(cols), formatRow(firstRow)]
      cnt = 1 # we already fetched and processed the first row
      for row in rs:
        cnt += 1
        if  limit is None or cnt <= limit:
          resultRep.append(formatRow(row))

      rs.close()

      if limit is not None and cnt > limit and cnt - limit > 0:
        resultRep.append(f"and {cnt - limit} more...")

      return "\n".join(resultRep)

  def execute(self, df):
    """
    Execute the operations and print results to stdout
    If pre-queries are necessary, e.g. for UDF or External table creation,
    they are executed first.

    Non-pretty mode outputs in CSV style -- the delim parameter can be used to 
    set the delimiter. Non-pretty mode ignores the maxColWidth parameter.
    """

    (pre,sql) = self.queryGenerator.generate(df)
    for pq in pre:
      # print(pq)
      self._execute(pq).close()
    # print(sql)
    return self._execute(sql)

  def _execAgg(self, df, col, func):
    """
    Actually compute the aggregation function.

    If we have a GROUP BY operation, the aggregation is only stored
    as a transformation and needs to be executed using show() or similar.

    If no grouping exists, we want to compute the aggregate over the complete
    table and return the scalar result directly
    """

    return self._doExecAgg(df, col, func)

  def _gen_agg(self, df, col, func):
    return self.queryGenerator._generateAggCode(df, col, func)

  def _doExecAgg(self, df, col, func):
    """
    Really executes the aggregation and returns the single result
    """
    (pre, aggQry) = self.queryGenerator._generateAggCode(df, col, func)
    for pq in pre:
      self._execute(pq).close()
    # execute an SQL query and get the result set
    rs = self._execute(aggQry)
    #fetch first (and only) row, return first column only
    return rs.fetchone()[0]  