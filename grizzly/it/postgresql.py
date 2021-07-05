import logging
import psycopg2

logger=logging.getLogger("test")

def connect(user: str, passwd: str, db: str, port: int):
  
  logger.debug(f"about to connect to PostgreSQL: {user}:{passwd} @ {db} on port {port}")
  con = psycopg2.connect(dbname=db, user=user, password=passwd,host="localhost",port=port)

  from sqlalchemy import create_engine
  engine = create_engine(f"postgresql+psycopg2://{user}:{passwd}@localhost:{port}/{db}")

  return (con,engine)