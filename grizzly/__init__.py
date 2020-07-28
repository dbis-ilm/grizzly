from grizzly.dataframes.frame import Table
from grizzly.dataframes.frame import ExternalTable
from grizzly.generator import GrizzlyGenerator

def use(backend):
  GrizzlyGenerator._backend = backend

def close():
  GrizzlyGenerator.close()

def read_table(tableName):
  return Table(tableName)

def read_external_files(file, colDefs, hasHeader=True, delimiter='|', format=""):
  return ExternalTable(file, colDefs, hasHeader, delimiter, format)