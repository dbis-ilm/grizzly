import sqlalchemy
from sqlalchemy.sql import select

class Connection(object):

    engine = None
    md = None
    @staticmethod
    def init(dbname, user, pw, host="localhost", port=5432):
        Connection.engine = sqlalchemy.create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{dbname}").connect()
        Connection.md = sqlalchemy.MetaData()

class Column(object):
    def __init__(self, relation, name, dtype,   table):
        self.relation = relation
        self.name = name
        self.dtype = dtype
        self.table = table

    def fqn(self):
        return f"{relation}.{name}"

    def __eq__(self, other):
        # print("eq function")
        expr = self.table.select(self.table.columns[self.name].__eq__(other))
        # print(str(expr))
        return expr

    def __str__(self): 
        return f"{self.relation}.{self.name}:{self.dtype}"

class DataFrame(object):

    @staticmethod
    def fromTable(tableName):
        # self.tableName = tableName
        table = sqlalchemy.Table(tableName, Connection.md, autoload=True, autoload_with=Connection.engine)
        
        columns = {}
        for c in table.columns:
            columns[c.name] = Column(tableName, c.name, c.type, table)

        return DataFrame(None, columns, table)


    def __init__(self, parent, columns, op):
        self.parent = parent
        self.op = op
        self.columns = columns

    def __getitem__(self, key):
        theType = type(key)

        # projection
        if theType is list:
            newDF = DataFrame(self, self.columns, self.op.select(key))
            return newDF
        elif theType is str:
            return self.columns[key]
        if theType is sqlalchemy.sql.selectable.Select:
            newDF = DataFrame(self, self.columns, self.op.select(key))
            return newDF
        else:
            print("blubb:"+str(theType))



    def __setitem__(self, key, value):
        pass


    # def _build(self):
    #     if self.parent is not None:
    #         return self.parent._build().op
    #     else:
    #         return op

    def sql(self):
        return str(self.op)

if __name__ == "__main__":

    Connection.init("","","","",5432)
    df = DataFrame.fromTable("sensors")

    # print(str(df.table.select(df.table.c.lat)))
    # print(str(select([df.table.c.lat]).where(True)))
    # print(df[df['country'] == 'hage'].sql())
    print(df['country'] == 'hage')