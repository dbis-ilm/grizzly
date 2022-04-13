import pandas as pd
def run(con, alchemyCon):
  o = pd.read_sql_table("orders", alchemyCon)
  
  c = pd.read_sql_table("customer", alchemyCon)
  l = pd.read_sql_table("lineitem", alchemyCon)

  # Filters
  c = c[c["c_mktsegment"].str.match("BUILDING")]
  o = o[o["o_orderdate"] < pd.to_datetime("1995-03-15")]
  l = l[l["l_shipdate"] > pd.to_datetime("1995-03-15")]
  l["calculated"] = l["l_extendedprice"] * ( 1 - l["l_discount"])

  # We do not have indexes, so we use merge instead of join, which has the same effect
  j = c.merge(o, left_on = "c_custkey", right_on="o_custkey")
  j = j.merge(l, left_on = "o_orderkey", right_on="l_orderkey")

  g = j.groupby(["l_orderkey", "o_orderdate", "o_shippriority"], as_index=False)["calculated"].sum().rename(columns={"calculated":"revenue"})
  g = g[["l_orderkey", "revenue", "o_orderdate", "o_shippriority"]] # bring cols in expected order
  g = g.sort_values(["l_orderkey", "revenue", "o_orderdate", "o_shippriority"])
  g = g.head(100)

  g["o_orderdate"] = g["o_orderdate"].dt.date.astype(str)
  # g["revenue"] = g["revenue"].round(decimals=4)
  return g