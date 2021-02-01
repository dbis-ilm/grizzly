import pandas as pd

#@profile
def csv():
    tab = pd.read_csv("/var/lib/postgresql/tpch-dbgen/orders_SIZE.tbl", names=["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate", "o_orderpriority","o_clerk", "o_shippriority", "o_comment"], header=None , sep='|', index_col=False)
    res = tab["o_totalprice"].min()
    print(res)
csv()
