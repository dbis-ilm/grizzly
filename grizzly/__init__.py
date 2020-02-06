from grizzly.dataframes.frame import Table
from grizzly.generator import GrizzlyGenerator

def use(backend):
  GrizzlyGenerator.generator = backend

def close():
  GrizzlyGenerator.close()


def read_table(tableName):
  
  # if connection is not None and Connection.db is None:
  #   Connection.db = connection

  # columns = []
  # for c in table.columns:
  #     columns.append(Column(tableName, c.name, c.type, table))

  # return DataFrame(columns, From(tableName))
  return Table(tableName)