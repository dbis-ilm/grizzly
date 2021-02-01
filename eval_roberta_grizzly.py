import grizzly
# Requires pyodbc and eventually unixodbc-dev for pyodbc build process
from grizzly.relationaldbexecutor import RelationalExecutor
from grizzly.sqlgenerator import SQLGenerator
from grizzly.aggregates import AggregateType
import psycopg2 as pg

con = pg.connect(user="postgres", password="password123", host="localhost", database="movies")
grizzly.use(RelationalExecutor(con, SQLGenerator("postgresql")))

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

onnx_path = "/var/lib/postgresql/roberta-sequence-classification.onnx"
df = grizzly.read_table("reviews_SIZE")
df["sentiment"] = df["review"].apply_onnx_model(onnx_path, input_to_tensor, tensor_to_output)
df = df.groupby(["sentiment"]).count("review")
df.show(pretty = True)

con.close()
