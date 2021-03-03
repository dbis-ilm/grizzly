import grizzly

def run(con, alchemyCon):
  df = grizzly.read_table("events")
  avg = df["globaleventid"].mean()
  return avg