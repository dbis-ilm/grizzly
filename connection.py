import sqlalchemy

class Connection(object):
    engine = None
    md = None
    @staticmethod
    def init(dbname, user, pw, host="localhost", port=5432):
        Connection.engine = sqlalchemy.create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{dbname}").connect()
        Connection.md = sqlalchemy.MetaData()
