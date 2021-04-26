import grizzly

def run(con, alchemyCon):
  orders = grizzly.read_external_files("grizzly/it/resources/orders.tbl.u1", ["o_orderkey:int, o_custkey:int, o_orderstatus:char(1), o_totalprice:float, o_orderdate:ansidate, o_orderpriority:str, o_clerk:str, o_shippriority:int, o_comment:str"], True, "|", "csv")
  customer = grizzly.read_table("customer")
  j1 = orders.join(customer, on = (orders.o_custkey == customer.c_custkey))
  a = j1.groupby("c_mktsegment").count()
  return a