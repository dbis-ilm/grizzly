from sqlalchemy.sql import select, column
import sqlalchemy
from sqlops import From, Filter, Projection
from column import Column, Eq, Expr
from connection import Connection

class DataFrame(object):

    @staticmethod
    def fromTable(tableName):
        # self.tableName = tableName
        table = sqlalchemy.Table(tableName, Connection.md, autoload=True, autoload_with=Connection.engine)
        
        # columns = {}
        # for c in table.columns:
        #     columns[c.name] = Column(tableName, c.name, c.type, table)

        # stmt = select([column('globaleventid')]).select_from(table).where(table.c.globaleventid == '1')
        # print(str(stmt))
        
        return DataFrame(table.c, table)


    def __init__(self, columns, op):
        # self.parent = parent
        self.op = op
        self.columns = columns

    def __getitem__(self, key):
        theType = type(key)

        # projection
        if theType is list:
            self.op =  self.op.select(key)
            return self
        elif theType is str:
            self.op = self.op.select(column(key))
            return self
        # elif theType is sqlalchemy.sql.selectable.Select:
            # newDF = DataFrame(self, self.columns, self.op.select(key))
            # return newDF
        elif isinstance(key, Eq):
            print("eq")
            self.op = self.op.where(key.left == key.right)
            return self
        else:
            print("blubb:"+str(theType))

    def __eq__(self,other):
        return Eq(self.columns.values()[0], other)
        

    # def __setitem__(self, key, value):

    # def _build(self):
    #     if self.parent is not None:
    #         return self.parent._build().op
    #     else:
    #         return op

    def sql(self):
        return str(self.op)

if __name__ == "__main__":

    # Connection.init("pfmegrnargs","reader","NWDMCE5xdipIjRrp","hh-pgsql-public.ebi.ac.uk",5432)
    Connection.init("grizzlytest","grizzly","grizzly","cloud04",54322)
    df = DataFrame.fromTable("gdeltevents")

    print(df[df['globaleventid'] == '1252385'].sql())