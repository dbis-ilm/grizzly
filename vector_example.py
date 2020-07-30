import grizzly
# Requires pyodbc and eventually unixodbc-dev for pyodbc build process
import pyodbc as pdb
from grizzly.relationaldbexecutor import RelationalExecutor

"""
    Connect to remote Vector instance
    Requires Ingres/Vector Client runtime.
    Set up vnode using netutils.
    Specify vnode name as 'server' attribute in connection string.
    For remote access, Vector installation must be configured as dmbs_authentication=OPTIONAL.
"""

con = pdb.connect("driver=Ingres;servertype=ingres;server=dbblade;database=tpch")
grizzly.use(RelationalExecutor(con))

def myfunc(a: int) -> int:
    if a > 0:
        return a+a
    else:
        return -1

df1 = grizzly.read_external_files("hdfs://172.21.249.73/user/actian/tpch100/nation.csv",
                                 ["n_nationkey:int", "n_name:str" , "n_regionkey:int", "n_comment:str"], False)
df2 = grizzly.read_table("region")
j = df1.join(df2, on = (df1.n_regionkey == df2.r_regionkey))

j["newkey"] = j[df2.r_regionkey].map(myfunc)
print(j.generateQuery())
j.show(pretty=True)