import connection
import frame

connection.Connection.init("pfmegrnargs","reader","NWDMCE5xdipIjRrp","hh-pgsql-public.ebi.ac.uk",5432)
df = frame.DataFrame2.fromTable("rna")

df = df[df['id'] == '1252385']


print(df[['userstamp','upi']].sql())
df[['userstamp','upi']].show()