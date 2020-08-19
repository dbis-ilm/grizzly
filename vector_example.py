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
grizzly.use(RelationalExecutor(con, SQLGenerator("vector")))

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

def input_to_tensor(input:str):
    import torch
    from transformers import RobertaForSequenceClassification, RobertaTokenizer
    def to_numpy(tensor):
        return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

    tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
    input_ids = torch.tensor(tokenizer.encode(input, add_special_tokens=True)).unsqueeze(0)  # Batch size 1
    ort_inputs = {random.onnx_session.get_inputs()[0].name: to_numpy(input_ids)}
    return ort_inputs

def tensor_to_output(tensor) -> str:
    import numpy as np
    pred = np.argmax(tensor)
    if (pred == 0):
        return("Negative")
    elif (pred == 1):
        return("Positive")

onnx_path = "/home/actian/roberta-sequence-classification.onnx"
df = grizzly.read_table("movies")
df["sentiment"] = df["review"].apply_onnx_model(onnx_path, input_to_tensor, tensor_to_output)
df.show()

con.close()