from frame import DataFrame2
from sqlops import From

def read_table(tableName):
  
  columns = []
  # for c in table.columns:
  #     columns.append(Column(tableName, c.name, c.type, table))

  return DataFrame2(columns, From(tableName))