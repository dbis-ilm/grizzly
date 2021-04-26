import pandas as pd
def run(con, alchemyCon):
  customer = pd.read_sql_table("customer",alchemyCon)
  orders = pd.read_csv("grizzly/it/resources/orders.tbl.u1", sep="|")
  print(len(orders))
  j1 = orders.set_index("o_custkey").join(customer.set_index("c_custkey"))
  a = j1.groupby(["c_mktsegment"])["o_orderkey"].count()
  return a