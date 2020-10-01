import grizzly
import sqlite3
from grizzly.relationaldbexecutor import RelationalExecutor
from grizzly.wrapper import wrapper
from grizzly.aggregates import AggregateType


con=wrapper.wrap(["./sample.xlsx","./sample.csv","./grizzly.db"])
grizzly.use(RelationalExecutor(con))

print("----------------show Excel Data sheet1------------------------")
dfexcel = grizzly.read_table("sheet1")
dfexcel.show(pretty=True)

print("----------------Aggregate function on excel------------------------")
g= dfexcel.groupby(["Country","Product"])
a = g.agg(col="Product",aggType=AggregateType.COUNT)

print(a.generate())
a.show(pretty=True)

print("---------------show Excel Data sheet2-------------------------")
dfexcel2 = grizzly.read_table("sheet2")
dfexcel2.show(pretty=True)

print("---------------join between two excel sheet-------------------------")
j= dfexcel.join(dfexcel2, on=(dfexcel.Segment == dfexcel2.Segment), how='inner')
print(j.generate())
j.show(pretty=True)

print("---------------Show csv data-------------------------")
dfcsv = grizzly.read_table("sample")
dfcsv.show(pretty=True)

print("---------------Aggregate SUM on CSV File-------------------------")
g2= dfcsv.groupby(["Segment"])
a2 = g2.agg(col="MonthNumber",aggType=AggregateType.SUM)

print(a2.generate())
a2.show(pretty=True)

print("---------------Join between Excel and csv-------------------------")
j2= dfexcel.join(dfcsv, on=(dfexcel.Segment == dfcsv.Segment), how="inner")

print(j2.generate())
j2.show(pretty=True)

print("---------------Show DB data-------------------------")

dfdb = grizzly.read_table("grizzly.sample")
dfdb.show(pretty=True)

print("---------------Join Between two different tables t2 and t1-------------------------")
dfdb1 = grizzly.read_table("grizzly.t1")
dfdb2 = grizzly.read_table("grizzly.t2")

j3= dfdb1.join(dfdb2, on=(dfdb1.actor1name == dfdb2.actor2name), how="inner")
print(j3.generate())
j3.show(pretty=True)


print("---------------Join Between db and csv-------------------------")
j3= dfdb.join(dfcsv, on=(dfdb.Segment == dfcsv.Segment), how="left outer")

print(j3.generate())
j3.show(pretty=True)

print("--------------Join between db and Excel--------------------------")
j4= dfdb.join(dfexcel, on=(dfdb.Segment == dfexcel.Segment), how="inner")

print(j4.generate())
j4.show(pretty=True)

