import grizzly

def run(con, alchemyCon):
  df = grizzly.read_table("events")
  return df.count()