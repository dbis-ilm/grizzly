def prioToInt(prio: str) -> int:
  if prio is None or len(prio) == 0:
    return None

  num = prio[0]
  return int(num)

import grizzly

def run(con, alchemyCon):
  df = grizzly.read_table("orders")
  df["prionum"] = df["o_orderpriority"].map(prioToInt)
  df = df[[df.prionum, df.o_orderkey]]
  df = df.limit(10)
  df = df.sort_values(by=["prionum","o_orderkey"])
  return df
