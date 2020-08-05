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

con = pdb.connect("driver=Ingres;servertype=ingres;server=cloud01;database=tpch")
grizzly.use(RelationalExecutor(con))

def myfunc(a: int) -> int:
    if a > 0:
        return a+a
    else:
        return -1

def concatNames(name: str, comment: str) -> str:
    
    if not name or name == "":
        name = "hallo"
    
    if not comment or comment == "":
        comment = "welt"

    return name + " "+comment


def runtimetest(i: int) -> str:
    import random
    
    if not hasattr(random,"myblubb2"):
        random.myblubb2 = True
        return "not exists"
    else:
        return "exists"

df1 = grizzly.read_external_files("/home/actian/tpch-dbgen/nation.csv",
                                 ["n_nationkey:int", "n_name:str" , "n_regionkey:int", "n_comment:str"], False)
df2 = grizzly.read_table("region")
df2.show()

j = df1.join(df2, on = (df1.n_regionkey == df2.r_regionkey))

# j["newkey"] = j[df2.r_regionkey].map(myfunc)
# j["concted"] = j[[df2.r_name, df2.r_comment]].map(concatNames)
j["accum"] = j[df2.r_regionkey].map(runtimetest)


# print(j.generateQuery())
j.show(pretty=True, limit=25)
con.close()