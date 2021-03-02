import pandas as pd
import psycopg2 as pg 

def sql():
    con = pg.connect(user="postgres", password="password123", host="localhost", database="tpch")
    sql = "Select * from orders_SIZE"
    tab = pd.read_sql(sql,con)
    res = tab["o_totalprice"].min()
    print(res)

from memory_profiler import memory_usage
mem_usage = memory_usage((sql, (), {}), max_usage=True,interval=.2, timeout=1, include_children=True)
print(mem_usage)

