# import sqlalchemy
from sqlops import From, Filter, Projection, Grouping
from column import Column, Eq, Expr
from connection import Connection
import query

class DataFrame2(object):
  @staticmethod
  def fromTable(tableName):
    # self.tableName = tableName
    # table = sqlalchemy.Table(tableName, Connection.md, autoload=True, autoload_with=Connection.engine)
    
    columns = []
    # for c in table.columns:
    #     columns.append(Column(tableName, c.name, c.type, table))

    return DataFrame2(columns, From(tableName))

  def __init__(self, columns, op):
    self.op = op
    self.columns = columns


#####################################################
### relational ops

  def filter(self, expr):
    self.op = Filter(expr, self.op)
    return self

  def project(self, attrs):
    # print(self)
    # print(attrs)
    # print("---------")
    op = Projection(attrs, self.op)
    newColumns = attrs #[col for col in self.columns if col.name in attrs]

    return DataFrame2(newColumns, op)


  # def join

  # def groupby(self, attrs):
  #   self.op = Grouping(attrs, self.op)
  #   return self

  def __getitem__(self, key):
    theType = type(key)

    if isinstance(key, Expr):
      # print(f"filter col: {key}")
      return self.filter(key)
    elif theType is str:
      # print(f"projection col: {key}")
      return self.project([key])
    elif theType is list:
      # print(f"projection list: {key}")
      return self.project(key)
    else:
      print(f"{key} has type {theType} -- ignoring")
      return self

#####################################################
### aggregates

  def min(self, col=None):
    return self._execAgg("min",col)


  def max(self, col=None):
    return self._execAgg("max",col)

  def mean(self, col=None):
    return self._execAgg('avg',col)

  def count(self, col=None):
    colName = "*"
    if col is not None:
      colName = col
    return self._execAgg("count",colName)

  def sum(self , col=None):
    return self._execAgg("sum", col)


  def _execAgg(self, func, col):

    colName = None
    if col is None:
      colName = self.columns[0]
    else:
      colName = col

    innerSQL = self.sql()
    aggSQL = f"SELECT {func}({colName}) FROM ({innerSQL}) as t"
    
    with Connection.engine.connect() as con:
      row = con.execute(sql)
      return row[0]


  def sql(self):
    
    qry = query.Query()

    currOp = self.op
    while currOp != None:
      
      if isinstance(currOp, Filter):
        qry.Filters.append(currOp)
      elif isinstance(currOp, Projection):
        qry.ProjList = currOp.attrs
      elif isinstance(currOp, From):
        qry.From.append(currOp.relation)


      currOp = currOp.parent

    return qry.sql()

  def show(self):
    with Connection.engine.connect() as con:
      rs = con.execute(self.sql())

      for row in rs:
        print(row)

################
# comparisons

  def __eq__(self, other):
    # print(f"eq on {self.columns[0]} and {other}")
    expr = Eq(self.columns[0], other)
    return expr