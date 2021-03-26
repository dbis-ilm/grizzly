from grizzly.dataframes.schema import Schema, SchemaError
from .dataframes.frame import Table
from .dataframes.frame import ExternalTable
from .generator import GrizzlyGenerator

def use(backend):
  GrizzlyGenerator._backend = backend

def close():
  GrizzlyGenerator.close()

def read_table(tableName, index=None, schema=None, inferSchema=False):

  if schema is None and not inferSchema:
    schema = Schema(None)
  elif schema is None and inferSchema:
    schemaTypes = GrizzlyGenerator._backend.getSchemaForObject(tableName)
    schema = Schema(schemaTypes)
  elif isinstance(schema, dict):
    schema = Schema.build(schema)
    # schema = Schema(schema)
  elif not isinstance(schema, Schema):
    raise SchemaError(f"invalid type for schema. Must be None|dict|Schema but got {type(schema)}")


  return Table(tableName, index, schema)

def read_external_files(file, colDefs, hasHeader=True, delimiter='|', fileFormat="", fdw_extension_name=""):
  assert fileFormat != "", "External file format must be specified"
  return ExternalTable(file, colDefs, hasHeader, delimiter, fileFormat, fdw_extension_name)