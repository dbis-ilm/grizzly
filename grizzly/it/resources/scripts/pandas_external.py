import pandas as pd
def run(con, alchemyCon):
  customer = pd.read_sql_table("customer",alchemyCon)
  orders = pd.read_csv("grizzly/it/resources/tpch/orders.tbl.u1", sep="|", names=["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate", "o_orderpriority", \
  "o_clerk", "o_shippriority", "o_comment"])
  j1 = orders.set_index("o_custkey").join(customer.set_index("c_custkey"))
  a = j1.groupby(["c_mktsegment"])["o_orderkey"].count()
  return a