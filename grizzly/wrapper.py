import sqlite3
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

class wrapper(object):

  def csvWrap(connection, seperator=","):
      conn = sqlite3.connect('file::memory:?cache=shared')
      pd.read_csv(connection, sep=seperator).to_sql('csv', conn, if_exists='replace', index=True)
      return conn

  def excelWrap(connection):
      conn = sqlite3.connect('file::memory:?cache=shared')
      df= pd.read_excel(connection, sheet_name=None)
      for table, db in df.items():
          db.to_sql(table,conn)
      return conn

  def wrap(listOfConnection):
      conn = sqlite3.connect('file::memory:?cache=shared')
      for connections in listOfConnection:
          if connections.lower().endswith('.csv'):
              pd.read_csv(connections, sep=",").to_sql(os.path.splitext(os.path.basename(connections))[0], conn, if_exists='replace', index=True)
          elif connections.lower().endswith(('.xlsx','.xls')):
              df= pd.read_excel(connections, sheet_name=None)
              for table, db in df.items():
                  db.to_sql(table,conn)
          elif connections.lower().endswith('.db'):
              c= conn.cursor();
              base=os.path.basename(connections)
              filename=os.path.splitext(base)[0]
              c.execute('ATTACH DATABASE "'+connections+'" as '+filename+'')
              conn.commit()
      return conn

