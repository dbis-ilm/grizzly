from grizzly.aggregates import AggregateType

from grizzly.sqlgenerator import SQLGenerator

class RelationalExecutor(object):
  
  def __init__(self, connection, sqlGenerator=SQLGenerator()):
    super().__init__()
    self.connection = connection
    self.sqlGenerator = sqlGenerator

  def generate(self, df):
    return self.sqlGenerator.generate(df)

  def _execute(self, sql):
    cursor = self.connection.cursor()
    cursor.execute(sql)
    return cursor

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
      table.append_row(row)

    rs.close()
    return str(table)

  def toString(self, df, delim=",", pretty=False, maxColWidth=20):
    rs = self.execute(df)

    cols = [dec[0] for dec in rs.description]
    

    if not pretty:
      strings = [delim.join(cols)]
      for row in rs:
        strings.append(delim.join([str(col) for col in row]))

      rs.close()
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
      
      for row in rs:
        resultRep.append(formatRow(row))

      rs.close()
      return "\n".join(resultRep)

  def execute(self, df):
    """
    Execute the operations and print results to stdout

    Non-pretty mode outputs in CSV style -- the delim parameter can be used to 
    set the delimiter. Non-pretty mode ignores the maxColWidth parameter.
    """

    sql = self.sqlGenerator.generate(df)
    return self._execute(sql)


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
    rs = self._execute(aggSQL)
    #fetch first (and only) row, return first column only
    return rs.fetchone()[0]  