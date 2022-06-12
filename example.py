import grizzly
from grizzly.relationaldbexecutor import RelationalExecutor
from grizzly.udfcompiler.test_udfs import Test_funcs

import sqlite3
import cx_Oracle
import psycopg2

con = sqlite3.connect("grizzly.db")

grizzly.use(RelationalExecutor(con))

df = grizzly.read_table("events")

df = df[df["globaleventid"] == 470747760] # filter
df = df[["actor1name","actor2name"]]

df.show(pretty=True)

print("----------------------------------------")

df1 = grizzly.read_table("t1")
df2 = grizzly.read_table("t2")

j  = df1.join(df2, on = (df1.actor1name == df2.actor2name) | (df1["actor1countrycode"] <= df2["actor2countrycode"]), how="left outer")
print(j.generate())
cnt = j.count()
print(f"join result contais {cnt} elments")

print("----------------------------------------")

df = grizzly.read_table("events")

print(df.count("actor2name"))

print("----------------------------------------")

from grizzly.aggregates import AggregateType
df = grizzly.read_table("events")
g = df.groupby(["year","actor1name"])

a = g.agg(col="actor2name", aggType=AggregateType.COUNT)
a.show()

print("----------------------------------------")
# Example for UDF compiling
# Define function to be translated
func = Test_funcs.for_loop
# Add your connection (PostgreSQL and Oracle supported)
con = cx_Oracle.connect()
con2 = psycopg2.connect()

# Define Grizzly DataFrame
grizzly.use(RelationalExecutor(con))
df = grizzly.read_table("udf_test")
df = df[df['test_id'] < 30]
df = df[["test_id", "test_text", "test_float", "test_number"]]

# Apply Function to grizzly dataframe as new Column "udf"
df["udf"] = df[["test_number"]].map(func, lang='sql', fallback=True)

df = df[df['udf'] < 30]

# Pandas fallback only implemented for df.show()
print(df.generateQuery())
df.show()