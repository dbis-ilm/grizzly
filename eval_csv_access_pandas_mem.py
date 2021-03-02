import pandas as pd

def csv():
    tab = pd.read_csv("/var/lib/postgresql/tpch-dbgen/orders_SIZE.tbl", names=["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate", "o_orderpriority","o_clerk", "o_shippriority", "o_comment"], header=None , sep='|', index_col=False)
    res = tab["o_totalprice"].min()
    print(res)

from memory_profiler import memory_usage
mem_usage = memory_usage((csv, (), {}), max_usage=True,interval=.2, timeout=1, include_children=True)
print(mem_usage)

