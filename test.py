import unittest
import sqlite3
# import monetdbe

import re

import grizzly
from grizzly.aggregates import AggregateType
from grizzly.sqlgenerator import SQLGenerator
from grizzly.relationaldbexecutor import RelationalExecutor

class CodeMatcher(unittest.TestCase):
  

  def matchSnipped(self, snipped, template, removeLinebreaks: bool = False):
    res, mapping, reason = self.doMatchSnipped(snipped.strip(), template.strip(),removeLinebreaks)
    if not res:
      mapstr = "with mapping:\n"
      for templ,tVar in mapping.items():
        mapstr += f"\t{templ} -> {tVar}\n"
      self.fail(f"Mismatch\nFound:    {snipped}\nExpected: {template}\nReason:\t{reason}\n{mapstr}")
      

  def doMatchSnipped(self, snipped, template, removeLinebreaks):
    replacements = {}
    pattern = re.compile("\$t[0-9]+")
    pattern2 = re.compile("_t[0-9]+")

    placeholders = pattern.findall(template)
    occurences = pattern2.findall(snipped)

    mapping = {}
    for p,o in zip(placeholders, occurences):
      if p not in mapping:
        mapping[p] = o
      elif p in mapping and mapping[p] != o:
        return False, mapping, f"Mapping error: {p} -> {mapping[p]} exists, but {p} -> {o} found"

    # if we get here, the occurences match the templates

    if len(placeholders) != len(occurences):
      return False, mapping, f"number of placeholders {len(placeholders)} does not match occurences {len(occurences)}"

    for (k,v) in mapping.items():
      template = template.replace(k,v)

    templateClean = template.replace("\n","").replace(" ","").lower()
    snippedClean = snipped.replace("\n","").replace(" ","").lower()
    
    matches = snippedClean == templateClean

    return matches, mapping, "Snipped does not match template" if not matches else ""


class DataFrameTest(CodeMatcher):

  def setUp(self):
    # c = monetdbe.connect("grizzly.mdbe")
    c = sqlite3.connect("grizzly.db")
    grizzly.use(RelationalExecutor(c, SQLGenerator("vector")))

  def tearDown(self):
    grizzly.close()

  def test_groupby(self):
    df = grizzly.read_table("events")
    g = df.groupby(["theyear","actor1name"])
    a = g.agg(col="actor2name", aggType=AggregateType.MEAN)
    
    # expected = "select $t0.theyear, $t0.actor1name, avg($t0.actor2name) from events $t0 group by $t0.theyear, $t0.actor1name"
    expected = "select $t1.theyear, $t1.actor1name, avg($t1.actor2name) from (select * from events $t0) $t1 group by $t1.theyear, $t1.actor1name"
    actual = a.generateQuery()

    self.matchSnipped(actual, expected)

  def test_New(self):
    df = grizzly.read_table("events")
    df = df["a"]
    df = df[df["a"] == 2]

    actual = df.generateQuery()
    expected = "select * from (select $t1.a from (select * from events $t0) $t1) $t2 where $t2.a = 2"

    self.matchSnipped(actual, expected)


  def test_selectStar(self):
    df = grizzly.read_table("events") 
    actual = df.generateQuery()
    expected = "select * from events $t0"
    self.matchSnipped(actual, expected)

  def test_selectCountStar(self):
    df = grizzly.read_table("events")
    actual = df.count()
    self.assertEqual(actual, 30354)


  def test_selectStarFilter(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 468189636]

    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1 where $t1.globaleventid = 468189636"

    self.matchSnipped(actual, expected)


  def test_selectStarFilterString(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 'abc']
    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1 where $t1.globaleventid = 'abc'"

    self.matchSnipped(actual, expected)

  def test_selectColumnWithFilter(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 468189636]
    df = df['goldsteinscale']

    actual = df.generateQuery()
    # expected = "select $t0.goldsteinscale from events $t0 where $t0.globaleventid = 468189636"
    expected = "select $t2.goldsteinscale from (select * from (select * from events $t0) $t1 where $t1.globaleventid = 468189636) $t2"

    self.matchSnipped(actual, expected)

  def test_selectCountCol(self):
    df = grizzly.read_table("events")
    cnt = df.count('actor2name')
    self.assertGreater(cnt, 0)

  def test_selectStarGroupBy(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == '468189636']
    g = df.groupby(["theyear","monthyear"])

    actual = g.generateQuery()
    expected = "select $t2.theyear, $t2.monthyear from (select * from (select * from events $t0) $t1 where $t1.globaleventid = '468189636') $t2 group by $t2.theyear, $t2.monthyear"

    self.matchSnipped(actual, expected)

  def test_groupByComputedCol(self):
    from grizzly.generator import GrizzlyGenerator
    oldGen = GrizzlyGenerator._backend.queryGenerator

    newGen = SQLGenerator("postgresql")
    GrizzlyGenerator._backend.queryGenerator = newGen

    def mymod(s: str) -> int:
      return len(s) % 2
    
    df = grizzly.read_table("nation")
    df["computed"] = df[df.n_name].map(mymod)
    df = df.groupby("computed")
    df = df.agg(col = "*", aggType = AggregateType.COUNT)
    
    actual = df.generateQuery()
    
    sql = "select computed, count(*) from (select *,mymod($t0.n_name) as computed from nation $t0) $t1 group by computed"

    expected = f"""create or replace function mymod(s varchar(255)) returns int language plpython3u as 'return len(s) % 2' parallel safe;{sql}"""

    GrizzlyGenerator._backend.queryGenerator = oldGen

    self.matchSnipped(actual, expected)


    

  def test_groupByWithAggTwice(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 476829606]
    g = df.groupby(["theyear","monthyear"])

    agged = g.agg(col="actor2geo_type", aggType=AggregateType.COUNT)
    
    aggActual = agged.generateQuery()
    aggExpected = "select $t2.theyear, $t2.monthyear, count($t2.actor2geo_type) from (select * from (select * from events $t0) $t1 where $t1.globaleventid = 476829606) $t2 group by $t2.theyear, $t2.monthyear"

    self.matchSnipped(aggActual, aggExpected)

  def test_groupByTableAgg(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 476829606]
    g = df.groupby(["theyear","monthyear"])

    a = g.count("monthyear")
    # print(f"cnt: {a}")
    self.assertEqual(a, 1)

  def test_groupByTableAggStar(self):
    df = grizzly.read_table("events") 
    g = df.groupby("theyear")

    a = g.count()
    # print(f"cnt: {a}")
    self.assertEqual(a, 3)

  def test_joinTest(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 470259271]

    df2 = grizzly.read_table("events")
    
    joined = df.join(other = df2, on=["globaleventid", "globaleventid"], how = "inner")

    actual = joined.generateQuery()
    # expected = "SELECT * FROM events $t1 inner join events $t2 ON $t1.globaleventid = $t2.globaleventid where $t1.globaleventid = 470259271"
    expected = "select * from (select * from (select * from events $t0) $t1 where $t1.globaleventid = 470259271) $t4 inner join (select * from events $t2) $t5 on $t4.globaleventid = $t5.globaleventid"

    self.matchSnipped(actual, expected)

    # self.assertGreater(joined.count(), 0)

  def test_complexJoin(self):
    df1 = grizzly.read_table("t1")
    df2 = grizzly.read_table("t2")

    j = df1.join(df2, on = (df1['a'] == df2['b']) & (df1['c'] <= df2['d']), how="left outer")

    # expected = "SELECT * FROM t1 $t0 LEFT OUTER JOIN t2 $t2 ON $t0.a = $t2.b AND $t0.c <= $t2.d".lower()
    expected = "select * from (select * from t1 $t1) $t1 left outer join (select * from t2 $t2) $t2 on $t1.a = $t2.b and $t1.c <= $t2.d"
    
    actual = j.generateQuery().lower()

    self.matchSnipped(actual, expected)

  def test_triJoin(self):
    df1 = grizzly.read_table("t1")
    df2 = grizzly.read_table("t2")
    df3 = grizzly.read_table("t3")
    df3 = df3[["b","d"]]
    j = df1.join(df2, on = (df1['a'] == df2['b']) & (df1['c'] <= df2['d']), how="left outer")
    
    j = j[[df1.m,df2.x]]
    
    j2 = j.join(df3, on = (j['m'] == df3['b']) & (j['x'] <= df3['d']), how="inner")

    actual = j2.generateQuery()
    # expected = "select $t1.m, $t2.x, $t4.b, $t4.d from t1 $t1 left outer join t2 $t2 on $t1.a = $t2.b and $t1.c <= $t2.d inner join (select $t3.b, $t3.d from t3 $t3) $t4 on $t1.m = $t4.b and $t1.x <= $t4.d"
    expected = "select * from (select $t2.m, $t2.x from (select * from (select * from t1 $t0) $t0 left outer join (select * from t2 $t1) $t1 on $t0.a = $t1.b and $t0.c <= $t1.d) $t2) $t2 inner join (select $t6.b, $t6.d from (select * from t3 $t4) $t6) $t6 on $t3.m = $t6.b and $t3.x <= $t6.d"
    self.matchSnipped(actual, expected)

  def test_DistinctAll(self):
    df = grizzly.read_table("events")
    df = df.distinct()
    actual = df.generateQuery()
    expected = "SELECT distinct * FROM (SELECT * from events $t0) $t1"
    self.matchSnipped(actual, expected)

  def test_DistinctOneCol(self):
    df = grizzly.read_table("events")
    df = df['isrootevent'].distinct()
    actual = df.generateQuery()
    # print(actual)
    expected = "select distinct $t1.isrootevent from (select * from events $t0) $t1"
    
    self.matchSnipped(actual, expected)
    # self.assertEqual

  def test_DistinctTwoCols(self):
    df = grizzly.read_table("events")
    df = df[['y',"x"]].distinct()
    actual = df.generateQuery()
    expected = "select distinct $t1.y, $t1.x from (select * from events $t0) $t1"
    self.matchSnipped(actual, expected)
    # print(df[['y',"x"]].distinct().sql())

  def test_Eq(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 468189636]
    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1  where $t1.globaleventid = 468189636"
    self.matchSnipped(actual, expected)

  def test_Ne(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] != 468189636]
    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1  where $t1.globaleventid <> 468189636"

    self.matchSnipped(actual, expected)

  def test_Lt(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] < 468189636]
    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1  where $t1.globaleventid < 468189636"
    self.matchSnipped(actual, expected)

  def test_Le(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] <= 468189636]
    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1  where $t1.globaleventid <= 468189636"

    self.matchSnipped(actual, expected)

  def test_Gt(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] > 468189636]
    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1  where $t1.globaleventid > 468189636"

    self.matchSnipped(actual, expected)

  def test_Ge(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] >= 468189636]
    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1  where $t1.globaleventid >= 468189636"
    self.matchSnipped(actual, expected)

  def test_collect(self):
    df = grizzly.read_table("events") 
    arr = df.collect(includeHeader=False)

    self.assertEqual(len(arr), 30354)

  def test_collectWithHeader(self):
    df = grizzly.read_table("events") 
    arr = df.collect(includeHeader=True)

    self.assertEqual(len(arr), 30354+1)

  def test_show(self):
    df = grizzly.read_table("events") 

    df = df[df['globaleventid'] <= 468189636 ]  #== 467268277
    df = df[["actor1name","actor2name", "globaleventid","sourceurl"]]

    from io import StringIO
    import sys
    try:
      bkp = sys.stdout
      sys.stdout = mystdout = StringIO()

      df.show(limit=None)

      output = mystdout.getvalue().splitlines()

      self.assertEqual(len(output), 2842+1) #+1 for column names

    finally:
      sys.stdout = bkp


  def test_showPretty(self):
    df = grizzly.read_table("events") 

    df = df[df['globaleventid'] <= 468189636]  #== 467268277
    df = df[["actor1name","actor2name", "globaleventid","sourceurl"]]

    from io import StringIO
    import sys
    try:
      bkp = sys.stdout
      sys.stdout = mystdout = StringIO()
      
      maxColWidth = 40

      df.show(pretty=True, maxColWidth = maxColWidth)

      output = mystdout.getvalue().splitlines()

      for row in output:
        for col in row:
          self.assertLessEqual(len(col), maxColWidth)

    finally:
      sys.stdout = bkp

  def test_toString(self):
    df = grizzly.read_table("events") 

    df = df[df['globaleventid'] == 467268277]
    df = df[["actor1name","actor2name", "globaleventid","sourceurl"]]

    strDF = str(df)
    splt = strDF.split("\n")

    rows = df.count()
    # print(rows)
    dfLen = len(splt)
    rowsLen = rows+ 3

    self.assertEqual(dfLen, rowsLen) # column names + top rule + bottom rule

  def test_ViewJoin(self):
    df1 = grizzly.read_table("t1")
    df2 = grizzly.read_table("t2")
    
    j  = df1.join(df2, on = (df1.actor1name == df2.actor2name) | (df1["actor1countrycode"] <= df2["actor2countrycode"]), how="left outer")
    cnt = j.count()
    self.assertEqual(cnt, 9899259)

  def test_udf(self):
    from grizzly.generator import GrizzlyGenerator
    oldGen = GrizzlyGenerator._backend.queryGenerator

    newGen = SQLGenerator("postgresql")
    GrizzlyGenerator._backend.queryGenerator = newGen

    # function must have "return annotation" so that we know 
    # what the result would be
    # parameters should also contain type annotation, e.g. 'a: int'
    # or may be named after the actual column (postgres lets you define the type
    # by referencing the column with `mytable.mycolumn%TYPE`)
    def myfunc(a: int) -> str:
      return a+"_grizzly"
    
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 467268277]
    df["newid"] = df["globaleventid"].map(myfunc)

    sql = "select *,myfunc($t1.globaleventid) as newid from (select * from events $t0) $t1 where $t1.globaleventid = 467268277"

    actual = df.generateQuery()

    expected = f"""create or replace function myfunc(a int) returns varchar(255) language plpython3u as 'return a+"_grizzly"' parallel safe;{sql}"""

    GrizzlyGenerator._backend.queryGenerator = oldGen

    self.matchSnipped(actual, expected, removeLinebreaks=True)


  # def test_udflambda(self):
  #   df = grizzly.read_table("events") 
  #   # df["newid"] = [df['globaleventid'] == 467268277]
  #   df["newid"] = df["globaleventid"].map(lambda x: x+"grizzlylambda")

  def test_mapDataFrame(self):
    df1 = grizzly.read_table("events") 
    df2 = grizzly.read_table("events") 

    j = df1.map(df2)

    actual = j.generateQuery()
    expected = "select * from (select * from events $t0) $t0 natural join (select * from events $t1) $t1"
    self.matchSnipped(actual, expected)

  
  # def test_predictPytorch(self):

  #   from grizzly.generator import GrizzlyGenerator
  #   oldGen = GrizzlyGenerator._backend.queryGenerator

  #   newGen = SQLGenerator("postgresql")
  #   GrizzlyGenerator._backend.queryGenerator = newGen

  #   def isEmptyString(s):
  #     return len(s) <= 0

  #   def stringToTensor(s):
  #     if not isEmptyString(s):
  #       return s.split()
  #     else:
  #       return []

  #   df = grizzly.read_table("events") 
  #   df["blubb"] = df[df.n_nation].apply_torch_model("/tmp/mymodel.pt", stringToTensor, clazzParameters=[],outputDict=["hallo"])

  #   actual = df.generateQuery()
  #   print(actual)

  #   GrizzlyGenerator._backend.queryGenerator = oldGen

  def test_externaltable(self):
    df = grizzly.read_external_files("filename.csv", ["a:int, b:str, c:float"], False)
    actual = df.generateQuery()
    expected = "DROP TABLE IF EXISTS temp_ext_table$t0;" \
               "CREATE EXTERNAL TABLE temp_ext_table$t0(a int, b VARCHAR(1024), c float) " \
               "USING SPARK WITH REFERENCE='filename.csv', OPTIONS=('delimiter'='|','header'='false','schema'='a int, b VARCHAR(1024), c float') " \
               "SELECT * FROM temp_ext_table$t0 $t0"
    self.matchSnipped(actual, expected)

    df = grizzly.read_external_files("filename.csv", ["a:int, b:str, c:float"], True)
    actual = df.generateQuery()
    expected = "DROP TABLE IF EXISTS temp_ext_table$t0;" \
               "CREATE EXTERNAL TABLE temp_ext_table$t0(a int, b VARCHAR(1024), c float) " \
               "USING SPARK WITH REFERENCE='filename.csv', OPTIONS=('delimiter'='|') " \
               "SELECT * FROM temp_ext_table$t0 $t0"
    self.matchSnipped(actual, expected)

    df = grizzly.read_external_files("filename.csv", ["a:int, b:str, c:float"], True, ',')
    actual = df.generateQuery()
    expected = "DROP TABLE IF EXISTS temp_ext_table$t0;" \
               "CREATE EXTERNAL TABLE temp_ext_table$t0(a int, b VARCHAR(1024), c float) " \
               "USING SPARK WITH REFERENCE='filename.csv', OPTIONS=('delimiter'=',') " \
               "SELECT * FROM temp_ext_table$t0 $t0"
    self.matchSnipped(actual, expected)

    df = grizzly.read_external_files("filename.csv", ["a:int, b:str, c:float"], True, ',', "csv")
    actual = df.generateQuery()
    expected = "DROP TABLE IF EXISTS temp_ext_table$t0;" \
               "CREATE EXTERNAL TABLE temp_ext_table$t0(a int, b VARCHAR(1024), c float) " \
               "USING SPARK WITH REFERENCE='filename.csv', FORMAT='csv', OPTIONS=('delimiter'=',') " \
               "SELECT * FROM temp_ext_table$t0 $t0"
    self.matchSnipped(actual, expected)

if __name__ == "__main__":
    unittest.main()
