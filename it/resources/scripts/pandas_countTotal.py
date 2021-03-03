import pandas as pd
def run(con, alchemyCon):
  df = pd.read_sql_table("events", alchemyCon)
  return len(df)