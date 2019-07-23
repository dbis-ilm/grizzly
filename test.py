import connection
import frame

# connection.Connection.init("pfmegrnargs","reader","NWDMCE5xdipIjRrp","hh-pgsql-public.ebi.ac.uk",5432)
connection.Connection.init("grizzlytest","grizzly","grizzly","cloud04",54322)
df = frame.DataFrame2.fromTable("gdeltevents20mio")

print(df.count())

df = df[df['globaleventid'] == '468189636']


df['goldsteinscale'].show()

print(f"count={df.count('actor2name')}")

print(f"max={df['globaleventid'].max()}")
print(f"min={df['globaleventid'].min()}")

print(f"min_col = {df.min('globaleventid')}")


g = df.groupby(["year","monthyear"])

g.show()
a = g.count("actor2geo_type")
m = g.mean("avgtone")

a.show()
m.show()

df2 = frame.DataFrame2.fromTable("miotest")
df3 = frame.DataFrame2.fromTable("miotest")
joined = df.join(other = df2, on=["globaleventid", "globaleventid"], how = "inner").join(other=df3, on=["actor2name", "actor2name"], how = "inner")



print(joined.count())

g2 = joined[joined['globaleventid'] == '468189636']

g2.show()