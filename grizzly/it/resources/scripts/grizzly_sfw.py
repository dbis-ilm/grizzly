import grizzly

def run(con, alchemyCon):
  df = grizzly.read_table("orders")
  df = df[df["o_orderstatus"] == "O"]
  df = df[["o_orderkey", "o_totalprice", "o_orderdate"]]
  return len(df)