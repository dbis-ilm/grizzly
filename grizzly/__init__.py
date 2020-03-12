from grizzly.dataframes.frame import Table
from grizzly.generator import GrizzlyGenerator

def use(backend):
  GrizzlyGenerator._backend = backend

def close():
  GrizzlyGenerator.close()

def read_table(tableName):
  return Table(tableName)