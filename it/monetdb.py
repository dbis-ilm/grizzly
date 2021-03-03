import typing
import pymonetdb
import logging

logger=logging.getLogger("test")

def connect(user: str, passwd: str, db: str, port: int):
  logger.debug(f"about to connect to MonetDB: {user}:{passwd} @ {db} on port {port}")
  
  con = pymonetdb.connect(username=user, password=passwd, hostname="localhost", database=db,port=port)

  from sqlalchemy import create_engine
  engine = create_engine(f"monetdb://{user}:{passwd}@localhost:{port}/{db}", echo=False)

  return (con,engine)