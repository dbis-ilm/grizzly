import grizzly
# Requires pyodbc and eventually unixodbc-dev for pyodbc build process
import pyodbc as pdb

import psycopg2 as pg

from grizzly.relationaldbexecutor import RelationalExecutor
from grizzly.sqlgenerator import SQLGenerator

"""
    Connect to remote Vector instance
    Requires Ingres/Vector Client runtime.
    Set up vnode using netutils.
    Specify vnode name as 'server' attribute in connection string.
    For remote access, Vector installation must be configured as dmbs_authentication=OPTIONAL.
"""

con = pg.connect("dbname=tpch_partitioned user=grizzly password=grizzly host=cloud01.prakinf.tu-ilmenau.de")
grizzly.use(RelationalExecutor(con, SQLGenerator("postgresql")))

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

from grizzly.sqlgenerator import SqlBigInt
def addkeys2(a: SqlBigInt, b:SqlBigInt) -> int:
    return a+b

def torchex(i: SqlBigInt) -> str:
    import torch

    return torch.__version__

def tfex(i: SqlBigInt) -> str:
    import tensorflow as tf

    return tf.__version__

import torch
class RNN(torch.nn.Module):
  def __init__(self, input_size, hidden_size, output_size):
    super(RNN, self).__init__()
    
    self.input_size = input_size
    self.hidden_size = hidden_size
    self.output_size = output_size
    
    self.i2h = torch.nn.Linear(input_size + hidden_size, hidden_size)
    self.i2o = torch.nn.Linear(input_size + hidden_size, output_size)
    self.softmax = torch.nn.LogSoftmax()
  
  def forward(self, input, hidden):
    combined = torch.cat((input, hidden), 1)
    hidden = self.i2h(combined)
    output = self.i2o(combined)
    output = self.softmax(output)
    return output, hidden

  def initHidden(self):
    return torch.autograd.Variable(torch.zeros(1, self.hidden_size))    

df1 = grizzly.read_table("region")    
# df1["new"] = df1[df1.r_regionkey].map(torchex)                        
# df2 = grizzly.read_table("lineitem")
# j = df1.join(df2, on = (df1.o_orderkey == df2.l_orderkey))

# j["newkey"] = j[df2.r_regionkey].map(myfunc)
# j["concted"] = j[[df2.r_name, df2.r_comment]].map(concatNames)
# j["accum"] = j[df2.r_regionkey].map(runtimetest)

# j["new"] = j[[df1.o_orderkey, df2.l_linenumber]].map(addkeys)


# print(j.generateQuery())
# j.show(pretty=False, limit=25)

# print(j.min("new"))
# maxsum = j.max("new")

def createoutputdict():
  return [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

outputdict = createoutputdict()

def line_to_tensor(line: str):
  import string
  all_letters = string.ascii_letters + " .,;"
  n_letters = len(all_letters)
  tensor = torch.zeros(len(line), 1, n_letters)
  for li, letter in enumerate(line):
      letter_index = all_letters.find(letter)
      tensor[li][0][letter_index] = 1
  return tensor


# df1["origin"] = df1[df1.r_name].predict("/names.pt",line_to_tensor,RNN, n_predictions=1)
df1["origin"] = df1[df1.r_name].predict("/model_dict.pt", toTensorFunc=line_to_tensor,clazz=RNN, outputDict=outputdict, n_predictions=1)

# df1["summed"] = df1[[df1.r_regionkey, df1.r_regionkey]].map(addkeys2)

print(df1.generateQuery())
df1.show(pretty=True)

# j2 = j[j.new == j.max("new")]
# j2.show(pretty=True, limit=25)
con.close()
