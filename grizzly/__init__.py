from .dataframes.frame import Table
from .dataframes.frame import ExternalTable
from .generator import GrizzlyGenerator

def use(backend):
  GrizzlyGenerator._backend = backend

def close():
  GrizzlyGenerator.close()

def read_table(tableName, index=None, schema=None):
  return Table(tableName, index, schema)

def read_external_files(file, colDefs, hasHeader=True, delimiter='|', format=""):
  return ExternalTable(file, colDefs, hasHeader, delimiter, format)