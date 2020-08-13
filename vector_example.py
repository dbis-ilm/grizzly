import grizzly
# Requires pyodbc and eventually unixodbc-dev for pyodbc build process
import pyodbc as pdb
from grizzly.relationaldbexecutor import RelationalExecutor
from grizzly.sqlgenerator import SQLGenerator

"""
    Connect to remote Vector instance
    Requires Ingres/Vector Client runtime.
    Set up vnode using netutils.
    Specify vnode name as 'server' attribute in connection string.
    For remote access, Vector installation must be configured as dmbs_authentication=OPTIONAL.
"""

con = pdb.connect("driver=Ingres;servertype=ingres;server=cloud01_docker;database=tpch")
grizzly.use(RelationalExecutor(con))

def myfunc(a: int) -> int:
    if a > 0:
        return a+a
    else:
        return -1

def addkeys(a: int, b:int) -> int:
    return a+b

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

"""
df1 = grizzly.read_table("orders")
df2 = grizzly.read_table("lineitem")
j = df1.join(df2, on = (df1.o_orderkey == df2.l_orderkey))
j["new"] = j[[df1.o_orderkey, df2.l_linenumber]].map(addkeys)
print(j.min("new"))



df1 = grizzly.read_external_files("file:///home/actian/tpch-dbgen/nation.csv",
                                 ["n_nationkey:int", "xn_name:str" , "n_regionkey:int", "n_comment:str"], False)
df2 = grizzly.read_table("region").apply_tensorflow_model(["The movie is great", None], checkpoint_dir, ["input_x", "dropout_keep_prob"], [None, 1.0], vocab_file)

j = df1.join(df2, on = (df1.n_regionkey == df2.r_regionkey))


vocab_file = "/home/sklaebe/workspace/cnn-text-classification-tf/runs/1596453054/vocab"
checkpoint_dir = "/home/sklaebe/workspace/cnn-text-classification-tf/runs/1596453054/checkpoints"

"""
vocab_file = "/home/actian/model/vocab"
checkpoint_file = "/home/actian/model/checkpoints/model-1000"
df1 = grizzly.read_table("movies")
df1["new"] = df1[df1.review].apply_tensorflow_model(checkpoint_file, ["input_x", "dropout_keep_prob"], [None, 1.0], vocab_file)
df1.show()

con.close()