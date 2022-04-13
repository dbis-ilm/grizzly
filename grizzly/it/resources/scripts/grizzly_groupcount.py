import grizzly

def run(con, alchemyCon):
  df = grizzly.read_table("orders")
  df = df[["o_orderkey", "o_orderstatus"]]
  df = df.groupby("o_orderstatus")
  df = df.count(df.o_orderkey, "cnt")
  df = df.sort_values(["o_orderstatus"])
  return df