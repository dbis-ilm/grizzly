import pandas as pd

def run(con, alchemyCon):
  df = pd.read_sql_table("events", alchemyCon)
  avg = df["globaleventid"].mean()
  return avg
