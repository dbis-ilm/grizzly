def prioToInt(prio: str) -> int:
  if prio is None or len(prio) == 0:
    return None

  num = prio[0]
  return int(num)

import pandas as pd
def run(con, alchemyCon):
  df = pd.read_sql_table("orders",alchemyCon)
  df["prionum"] = df["o_orderpriority"].map(prioToInt)
  df = df[[ "prionum", "o_orderkey"]]
  df = df.head(10)
  return df