import logging
import pyodbc as pdb

logger=logging.getLogger("test")

def connect(user: str, passwd: str, db: str, port: int):
  import time
  logger.debug(f"about to connect to Vector: {user}:{passwd} @ {db} on port {port}")
  # con = pdb.connect(f"driver=Ingres;servertype=ingres;server=edbt;database={db}")
  con = pdb.connect(f"driver=Ingres;servertype=ingres;server=@localhost,tcp_ip,{port};uid={user};pwd={passwd};database={db}")

  from sqlalchemy import create_engine
  engine = create_engine(f"ingres://{user}:{passwd}@127.0.0.1:{port}/{db}")


  return (con,engine)