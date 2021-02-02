import grizzly
import psycopg2 as pg
from grizzly.relationaldbexecutor import RelationalExecutor
from grizzly.sqlgenerator import SQLGenerator

#@profile
def sql():
    con = pg.connect(user="postgres", password="password123", host="localhost", database="tpch")
    grizzly.use(RelationalExecutor(con, SQLGenerator("postgresql")))
    tab = grizzly.read_table("orders_SIZE")
    res = tab.min("o_totalprice")
    print(res)

sql()
