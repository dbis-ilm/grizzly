import pandas as pd
import random
import onnxruntime
import psycopg2 as pg

def apply(input:str) -> str:
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


  def apply_model(input):
    if not hasattr(random, "onnx_session"):
        random.onnx_session = onnxruntime.InferenceSession("/var/lib/postgresql/roberta-sequence-classification.onnx")
    inputs = input_to_tensor(input)
    ret = random.onnx_session.run(None, inputs)
    return(tensor_to_output(ret))
  return apply_model(input)

con = pg.connect(user="postgres", password="password123", host="localhost", database="movies")
sql = "Select * from review_SIZE"
df = pd.read_sql(sql,con)
df["sentiment"] = df["review"].apply(apply)
df = df.groupby(["sentiment"])["review"].count()
print(df)

con.close()
