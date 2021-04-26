import pandas as pd
def run(con, alchemyCon):
  df = pd.read_sql_table("orders",alchemyCon)
  df = df[["o_orderkey", "o_orderstatus"]]
  df = df.groupby("o_orderstatus")["o_orderkey"].count().reset_index()
  return df