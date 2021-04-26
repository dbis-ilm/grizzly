import random


def input_to_tensor(input:str):
  import torch
  from transformers import RobertaForSequenceClassification, RobertaTokenizer
  def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()
  tokenizer = RobertaTokenizer.from_pretrained("/home/actian/EDBT2021_grizzly/myroberta")
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

from grizzly.aggregates import AggregateType
onnx_path = "/home/actian/EDBT2021_grizzly/roberta-sequence-classification.onnx"

import grizzly

def run(con, alchemyCon):
  df = grizzly.read_table("reviews_10")
  df["sentiment"] = df["review"].apply_onnx_model(onnx_path,input_to_tensor, tensor_to_output)
  agg = df.groupby(["sentiment"]).agg(AggregateType.COUNT, col="review")
  return agg