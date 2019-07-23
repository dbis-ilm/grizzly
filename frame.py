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

  def groupby(self, attrs):
    # self.op = Grouping(attrs, self.op)
    # return self
    self.op = Grouping(attrs, self.op )
    return DataFrame2(self.columns,  self.op)

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

    funcCode = f"{func}({colName})"  

    if isinstance(self.op, Grouping):
      newOp = Grouping(self.op.groupcols, self.op.parent)
      newOp.setAggFunc(funcCode)
      
      return DataFrame2(self.columns, newOp)
      
    else:
      return self._doExecAgg(funcCode)
    

  def _doExecAgg(self, funcCode):
    innerSQL = self.sql()
    aggSQL = f"SELECT {funcCode} FROM ({innerSQL}) as t"
    
    rs = self._doExecQuery(aggSQL)
    #fetch first (and only) row, return first column only
    return rs.fetchone()[0] 


  def _doExecQuery(self, qry):
    with Connection.engine.connect() as con:
      rs = con.execute(qry)
      return rs

  def sql(self):
    """
    Produce a SQL string from the current operator tree
    """

    qry = query.Query()

    currOp = self.op
    while currOp != None:
      
      if isinstance(currOp, Filter):
        qry.filters.append(currOp)
      elif isinstance(currOp, Projection):
        qry.projList = currOp.attrs
      elif isinstance(currOp, From):
        qry.froms.append(currOp.relation)
      elif isinstance(currOp, Grouping):
        qry.groupcols.extend(currOp.groupcols)
        qry.groupagg = currOp.aggFunc

      currOp = currOp.parent

    return qry.sql()

  def show(self):
    """
    Execute the operations and print results to stdout
    """

    qry = self.sql()

    print(qry)

    with Connection.engine.connect() as con:
      rs = con.execute(qry)

      for row in rs:
        print(row)

################
# comparisons

  def __eq__(self, other):
    # print(f"eq on {self.columns[0]} and {other}")
    expr = Eq(self.columns[0], other)
    return expr