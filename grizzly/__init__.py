from grizzly.frame import DataFrame
from grizzly.sqlops import From
from grizzly.connection import Connection


def read_table(tableName, connection = None):
  
  if connection is not None and Connection.db is None:
    Connection.db = connection

  columns = []
  # for c in table.columns:
  #     columns.append(Column(tableName, c.name, c.type, table))

  return DataFrame(columns, From(tableName))