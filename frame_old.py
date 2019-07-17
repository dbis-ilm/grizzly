from sqlalchemy.sql import select
import sqlalchemy
from sqlops import From, Filter, Projection
from column import Column, Eq, Expr
from connection import Connection

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
        elif theType is sqlalchemy.sql.selectable.Select:
            newDF = DataFrame(self, self.columns, self.op.select(key))
            return newDF
        elif isinstance(key, Expr):
            newDF = DataFrame(self, self.columns, self.op.where(key.left == key.right))
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

    Connection.init("pfmegrnargs","reader","NWDMCE5xdipIjRrp","hh-pgsql-public.ebi.ac.uk",5432)
    df = DataFrame.fromTable("rna")

    print(df[df['id'] == '1252385'].sql())