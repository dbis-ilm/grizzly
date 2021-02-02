import pandas as pd
import psycopg2 as pg 

#@profile
def sql():
    con = pg.connect(user="postgres", password="password123", host="localhost", database="tpch")
    sql = "Select * from orders_SIZE"
    tab = pd.read_sql(sql,con)
    res = tab["o_totalprice"].min()
    print(res)

sql()
