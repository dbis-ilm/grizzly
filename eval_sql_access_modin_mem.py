import psycopg2 as pg

def sql():
    import urllib
    sql = "Select * from orders_SIZE"
    #Parallel read with urllib-type connections. Note: Returns wrong results for partitioned tables.
    tab = pd.read_sql(sql, "postgresql://postgres:password123@localhost:5432/tpch")
    res = tab["o_totalprice"].min()
    print(res)


if __name__ == '__main__':
    import os
    #os.environ["MODIN_CPUS"] = "12"
    os.environ["MODIN_OUT_OF_CORE"] = "true"
    os.environ["MODIN_ENGINE"] = "ray"
    import modin.pandas as pd
    from memory_profiler import memory_usage
    mem_usage = memory_usage((sql, (), {}), max_usage=True,interval=.2, timeout=1, include_children=True)
    print(mem_usage)

