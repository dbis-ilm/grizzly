import grizzly

def run(con, alchemyCon):
  o = grizzly.read_table("orders")
  c = grizzly.read_table("customer")
  l = grizzly.read_table("lineitem")

  # Filters
  c = c[c["c_mktsegment"] == "BUILDING"]
  o = o[o["o_orderdate"] < "1995-03-15"]
  l = l[l["l_shipdate"] > "1995-03-15"]
  # This is a bit odd, we can do ColRef - constant, but not constant - ColRef. 
  l["calculated"] = l.L_EXTENDEDPRICE * ( (l.L_DISCOUNT * -1) + 1)

  # Joins
  j = c.join(o, on = ["c_custkey", "o_custkey"])
  j = j.join(l, on = ["o_orderkey", "l_orderkey"])

  # Aggregating and sorting
  g = j.groupby(["l_orderkey", "o_orderdate", "o_shippriority"])
  g = g.sum("calculated", "revenue")
  g = g[["l_orderkey", "revenue", "o_orderdate", "o_shippriority"]] # bring cols in expected order
  # g = g.sort_values(["revenue desc", "o_orderdate"])
  g = g.limit(100)
  return g