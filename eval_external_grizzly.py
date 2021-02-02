import grizzly
import psycopg2 as pg
from grizzly.relationaldbexecutor import RelationalExecutor
from grizzly.sqlgenerator import SQLGenerator

con = pg.connect(user="postgres", password="password123", host="localhost", database="tpch")
grizzly.use(RelationalExecutor(con, SQLGenerator("postgresql")))
orders = grizzly.read_external_files("/var/lib/postgresql/tpch-dbgen/orders_SIZE.tbl", ["o_orderkey:int, o_custkey:int, o_orderstatus:char(1), o_totalprice:float, o_orderdate:date, o_orderpriority:str, o_clerk:str, o_shippriority:int, o_comment:str"], True, "|", "csv", "file_fdw")
customer = grizzly.read_table("customer")
j1 = orders.join(customer, on = (orders.o_custkey == customer.c_custkey))
a = j1.groupby("c_mktsegment").count()
a.show()
