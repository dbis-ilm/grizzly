import pandas as pd
def run(con, alchemyCon):
  df =pd.read_sql_table("orders",alchemyCon)
  df = df[df["o_orderstatus"] == "O"]
  df = df[["o_orderkey", "o_totalprice", "o_orderdate"]]
  return len(df)