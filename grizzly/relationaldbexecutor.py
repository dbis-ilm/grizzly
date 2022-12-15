# from grizzly.generator import GrizzlyGenerator
from unicodedata import decimal
from grizzly.sqlgenerator import SQLGenerator
# Imports needed for getting the db vendor
import sqlite3
import cx_Oracle
import psycopg2

import logging
from typing import List
from decimal import Decimal

logger = logging.getLogger(__name__)

class RelationalExecutor(object):
  
  def __init__(self, connection, queryGenerator=None):
    self.connection = connection
    # Create SQLGenerator with known connection type
    # Creates dependencies for cx_oracle and postgresql packages, if not wanted,
    # profile for SQLGenerator must be defined manually for udf compiler
    # another approach could be to try to execute vendorspecific sql statements
    if not queryGenerator:
      if type(connection) == cx_Oracle.Connection:
        self.queryGenerator = SQLGenerator('oracle')
      elif type(connection) == psycopg2.extensions.connection:
        self.queryGenerator = SQLGenerator('postgresql')
      elif type(connection) == sqlite3.Connection:
        self.queryGenerator = SQLGenerator('sqlite')
      else:
        self.queryGenerator = SQLGenerator()
    else:
      self.queryGenerator = queryGenerator
    super().__init__()

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

  def getSchemaForObject(self, objName: str):
    (qry, namesColIdx, typesColIdx) = self.queryGenerator.getTableSchema(objName)
    if qry is None:
      return None

    dtypes = {}
    rs = self._execute(qry)
    for row in rs:
      colName = row[namesColIdx]
      colType = row[typesColIdx]

      dtypes[colName] = type(self.queryGenerator)._mapFromSQLTypes(str(colType))

    rs.close()

    return dtypes


  def fetchone(self, df):
    rs = self.execute(df)
    return rs.fetchone()

  def collect(self, df, includeHeader):
    rs = self.execute(df)

    tuples = []

    if includeHeader:
      cols = RelationalExecutor.__getHeader(rs)
      tuples.append(cols)

    def convert(i):
      t = type(i)
      if t is int or t is float or t is str or t is bool:
        return i
      elif isinstance(i, Decimal):
        return float(i)
      else:
        return str(i)

    for row in rs:
      # if the driver returns the tuple as some specialiced class (e.g. a Row implementation) 
      # we hide this by converting it into a Python list
      rowAsList = [convert(elem) for elem in row]
      tuples.append(rowAsList)

    return tuples

  def iterator(self, df, includeHeader):
    '''
    Returns an iterator over the result of the DF
    If includeHeader is true, the first row to be returned are the column names
    '''
    rs = self.execute(df)

    if includeHeader:
      yield RelationalExecutor.__getHeader(rs)

    for row in rs:
      yield row

  @staticmethod
  def __getHeader(rs) -> List[str]:
    if rs.description:
      cols = [dec[0] for dec in rs.description]
    else:
      cols = []
    return cols

  def table(self,df,limit=10):
    rs = self.execute(df)
    import beautifultable
    table = beautifultable.BeautifulTable()

    header = RelationalExecutor.__getHeader(rs)
    table.columns.header = header

    cnt = 0
    for row in rs:

      if cnt > limit:
        break

      cnt += 1
      table.rows.append(row)

    rs.close()
    return str(table)

  def toString(self, df, delim=",", pretty=False, maxColWidth=20, limit=20):
    rs = self.execute(df)

    cols = RelationalExecutor.__getHeader(rs)

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

  def to_df(self, df):
    (pre, qry) = self.queryGenerator.generate(df)
    import pandas
    p_df = pandas.read_sql(qry, self.connection)
    return p_df

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

  def _execAgg(self, df, f):
    """
    Really executes the aggregation and returns the single result
    """
    (pre, aggQry) = self.queryGenerator._generateAggCode(df, f)
    for pq in pre:
      self._execute(pq).close()
    # execute an SQL query and get the result set
    rs = self._execute(aggQry)
    #fetch first (and only) row, return first column only
    return rs.fetchone()[0]  

  def _gen_agg(self, df, func):
    return self.queryGenerator._generateAggCode(df, func)

