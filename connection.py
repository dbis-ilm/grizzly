import sqlalchemy

class Connection(object):
    engine = None
    md = None
    @staticmethod
    def init(connnectionString):
        Connection.engine = sqlalchemy.create_engine(connnectionString).connect()
        Connection.md = sqlalchemy.MetaData()
