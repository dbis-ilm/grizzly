import grizzly
import psycopg2 as pg
from grizzly.relationaldbexecutor import RelationalExecutor
from grizzly.sqlgenerator import SQLGenerator

def csv():
    con = pg.connect(user="postgres", password="password123", host="localhost", database="tpch")
    grizzly.use(RelationalExecutor(con, SQLGenerator("postgresql")))
    tab = grizzly.read_external_files("/var/lib/postgresql/tpch-dbgen/orders_SIZE.tbl", ["o_orderkey:int, o_custkey:int, o_orderstatus:char(1), o_totalprice:float, o_orderdate:date, o_orderpriority:str, o_clerk:str, o_shippriority:int, o_comment:str"], True, '|', "csv", "file_fdw")
    res = tab.min("o_totalprice")
    print(res)

from memory_profiler import memory_usage
mem_usage = memory_usage((csv, (), {}), max_usage=True,interval=.2, timeout=1, include_children=True)
print(mem_usage)
