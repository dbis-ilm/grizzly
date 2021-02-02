import pandas as pd
import psycopg2 as pg

con = pg.connect(user="postgres", password="password123", host="localhost", database="tpch")
sql = "Select * from customer"
customer = pd.read_sql(sql,con)
orders = pd.read_csv("/var/lib/postgresql/tpch-dbgen/orders_SIZE.tbl", names=["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate", "o_orderpriority","o_clerk", "o_shippriority", "o_comment"], header=None, sep="|")
j1 = orders.set_index("o_custkey").join(customer.set_index("c_custkey"))
a = j1.groupby(["c_mktsegment"])["o_orderkey"].count()
print(a)
