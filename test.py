import connection
import frame

# connection.Connection.init("pfmegrnargs","reader","NWDMCE5xdipIjRrp","hh-pgsql-public.ebi.ac.uk",5432)
connection.Connection.init("grizzlytest","grizzly","grizzly","cloud04",54322)
df = frame.DataFrame2.fromTable("gdeltevents20mio")

# df = df[df['globaleventid'] == '468189636']


# df['goldsteinscale'].show()

# print(f"count={df.count()}")

print(f"max={df['globaleventid'].max()}")
print(f"min={df['globaleventid'].min()}")

# print(df[['userstamp','upi']].sql())
# print(df['userstamp'].max().sql())

