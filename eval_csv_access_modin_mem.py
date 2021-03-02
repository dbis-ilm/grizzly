import psycopg2 as pg

def csv():
    tab = pd.read_csv("/var/lib/postgresql/tpch-dbgen/orders_SIZE.tbl", names=["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate", "o_orderpriority","o_clerk", "o_shippriority", "o_comment"], sep='|', index_col=False, header=None)
    res = tab["o_totalprice"].min()
    print(res)


if __name__ == '__main__':
    import os
    #os.environ["MODIN_CPUS"] = "12"
    os.environ["MODIN_OUT_OF_CORE"] = "true"
    os.environ["MODIN_ENGINE"] = "ray"
    import modin.pandas as pd
    from memory_profiler import memory_usage
    mem_usage = memory_usage((csv, (), {}), max_usage=True,interval=.2, timeout=1, include_children=True)
    print(mem_usage)

