from grizzly.expression import ExpressionException
import unittest
import sqlite3

import re

import grizzly
from grizzly.aggregates import AggregateType
from grizzly.sqlgenerator import SQLGenerator
from grizzly.relationaldbexecutor import RelationalExecutor

class CodeMatcher(unittest.TestCase):
  

  def matchSnipped(self, snipped, template, removeLinebreaks: bool = False):
    res, mapping, reason = CodeMatcher.doMatchSnipped(snipped.strip(), template.strip(),removeLinebreaks)
    if not res:
      mapstr = "with mapping:\n"
      for templ,tVar in mapping.items():
        mapstr += f"\t{templ} -> {tVar}\n"
      self.fail(f"Mismatch\nFound:    {snipped}\nExpected: {template}\nReason:\t{reason}\n{mapstr}")
      

  @staticmethod
  def doMatchSnipped(snipped, template, removeLinebreaks):
    pattern = re.compile(r"\$t[0-9]+")
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
    c = sqlite3.connect("grizzly.db")
    gen = SQLGenerator("sqlite")
    executor = RelationalExecutor(c, gen)
    grizzly.use(executor)

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

  def test_Having(self):
    df = grizzly.read_table("events")
    g = df.groupby(["theyear","actor1name"])
    a = g.agg(col="actor2name", aggType=AggregateType.COUNT,alias="cnt_actor")
    f = a.filter(a["cnt_actor"] > 2)
    
    expected = "select $t1.theyear, $t1.actor1name, count($t1.actor2name) as cnt_actor from (select * from events $t0) $t1 group by $t1.theyear, $t1.actor1name having cnt_actor > 2"
    actual = f.generateQuery()

    self.matchSnipped(actual, expected)

  def test_HavingExec(self):
    df = grizzly.read_table("events")
    g = df.groupby(["actor1name"])
    a = g.agg(col="actor2name", aggType=AggregateType.COUNT,alias="cnt_actor")
    f = a.filter(a["cnt_actor"] > 2)
    
    actual = f.collect()
    self.assertEqual(len(actual), 872)

    failedTuples = []
    for (actor1name,cnt_actor) in actual:
      if cnt_actor > 2:
        failedTuples.append( (actor1name, cnt_actor) )

    if len(failedTuples) <= 0:
      msg = ",".join(failedTuples)
      self.fail(f"tuples not matching having clause: {msg}")

  def test_groupByTableAggComputedCol(self):
    df = grizzly.read_table("events")
    g = df.groupby(["theyear","actor1name"])
    g["cnt_actor"] = g.count("actor2name") # FIXME: should not trigger execution but add the function to projection
    g["min_actor"] = g.min(g.actor2name) 

    expected = "select $t1.theyear, $t1.actor1name, count($t1.actor2name) as cnt_actor, min($t1.actor2name) as min_actor from (select * from events $t0) $t1 group by $t1.theyear, $t1.actor1name"
    actual = g.generateQuery()

    self.matchSnipped(actual, expected)

  def test_HavingTwice(self):
    df = grizzly.read_table("events")
    g = df.groupby(["theyear","actor1name"])
    a = g.agg(col="actor2name", aggType=AggregateType.COUNT,alias="cnt_actor")
    a = a.agg(col="actor2name", aggType=AggregateType.MIN,alias="min_actor")
    f = a.filter(a["cnt_actor"] > 2)
    f = f.filter(a["min_actor"] > 10)

    expected = "select $t1.theyear, $t1.actor1name, count($t1.actor2name) as cnt_actor, min($t1.actor2name) as min_actor from (select * from events $t0) $t1 group by $t1.theyear, $t1.actor1name having cnt_actor > 2 and min_actor > 10"
    actual = f.generateQuery()

    self.matchSnipped(actual, expected)

  def test_HavingTwiceExpr(self):
    df = grizzly.read_table("events")
    g = df.groupby(["theyear","actor1name"])
    a = g.agg(col="actor2name", aggType=AggregateType.COUNT,alias="cnt_actor")
    a = a.agg(col="actor2name", aggType=AggregateType.MIN,alias="min_actor")
    f = a.filter((a["cnt_actor"] > 2) & (a["min_actor"] > 10))

    expected = "select $t1.theyear, $t1.actor1name, count($t1.actor2name) as cnt_actor, min($t1.actor2name) as min_actor from (select * from events $t0) $t1 group by $t1.theyear, $t1.actor1name having cnt_actor > 2 and min_actor > 10"
    actual = f.generateQuery()

    self.matchSnipped(actual, expected)

  def test_ComputedExpr(self):
    df = grizzly.read_table("events")
    df = df[df.globaleventid == 476829606]
    df["newcol"] = df.theyear + df.monthyear

    df = df[[df.newcol, df.theyear, df.monthyear]]
    res = df.collect()

    self.assertEqual(len(res), 1)
    self.assertEqual(len(res[0]), 3)

    theYear = 2015
    monthYear = 201510

    self.assertEqual(res[0][1], theYear)
    self.assertEqual(res[0][2], monthYear)

    self.assertEqual(res[0][0], theYear + monthYear)


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

    expected = f"""create or replace function mymod(s varchar(1024)) returns int language plpython3u as 'return len(s) % 2' parallel safe;{sql}"""

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

  def test_groupByAggGroupCol(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 476829606]
    g = df.groupby(["theyear","monthyear"])

    cnt = g.count("monthyear", "cnt")
    # expected = "select count($t2.monthyear) as cnt from (select $t1.theyear, $t1.monthyear from (select * from (select * from events $t3) $t0 where $t0.globaleventid = 476829606) $t1 group by $t1.theyear, $t1.monthyear) $t2"
    # self.matchSnipped(actual, expected)

    self.assertEqual(cnt, 1)

  def test_groupByAggGroupColCode(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 476829606]
    g = df.groupby(["theyear","monthyear"])

    actual = g.agg(col="monthyear", aggType=AggregateType.COUNT, alias="cnt").generateQuery()

    expected = "select count($t2.monthyear) as cnt from (select $t1.theyear, $t1.monthyear from (select * from (select * from events $t3) $t0 where $t0.globaleventid = 476829606) $t1 group by $t1.theyear, $t1.monthyear) $t2"
    self.matchSnipped(actual, expected)


  def test_groupByAgg(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 476829606]
    g = df.groupby(["theyear","monthyear"])

    a = g.count("actor1name", "cnt")
    
    self.assertEqual(len(a.collect()),1)

  def test_groupByAggLimit(self):
    df = grizzly.read_table("events")
    df1 = df[(df.globaleventid < 470259271) & (df.actor1name != None)]
    df1 = df1.groupby(df1.actor1name)
    df1 = df1.count(df1.actor2name, alias="cnt_actor2")
    df1 = df1[:2]
    
    actual = df1.generateQuery()

    expected = "select $t3.* from (select $t2.actor1name, count($t2.actor2name) as cnt_actor2 from (select * from (select * from events $t0) $t1 where $t1.globaleventid < 470259271 and $t1.actor1name is not null) $t2 group by $t2.actor1name) $t3 LIMIT 2"

    self.matchSnipped(actual, expected)

  def test_groupByCountGroups(self):
    df = grizzly.read_table("events") 
    g = df.groupby("theyear")

    a = g.count("theyear")
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
    j = df1.join(df2, on = (df1['a'] == df2['b']) & (df1['c'] <= df2['d']) , how="left outer")

    # expected = "SELECT * FROM t1 $t0 LEFT OUTER JOIN t2 $t2 ON $t0.a = $t2.b AND $t0.c <= $t2.d".lower()
    expected = "select * from (select * from t1 $t1) $t3 left outer join (select * from t2 $t2) $t4 on $t3.a = $t4.b and $t3.c <= $t4.d"
    
    actual = j.generateQuery()

    self.matchSnipped(actual, expected)
  
  def test_complexWhere(self):
    df = grizzly.read_table("t1")
    expr = (df['a'] == df['b']) & (df['c'] <= df['d'])
    df = df[expr]

    expected = "select * from (select * from t1 $t1) $t2 where $t2.a = $t2.b and $t2.c <= $t2.d"
    actual = df.generateQuery()

    self.matchSnipped(actual, expected)

  def test_parenthisExpr(self):
    df = grizzly.read_table("t1")
    expr = (df['a'] == df['b']) & ((df['c'] <= df['d']) | ((df.f > 3) & (df.e != None)))
    df = df[expr]

    actual = df.generateQuery()
    expected = "select * from (select * from t1 $t1) $t2 where $t2.a = $t2.b and ($t2.c <= $t2.d or ($t2.f > 3 and $t2.e is not NULL))"

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

  def test_EqNone(self):
    df = grizzly.read_table("events") 
    df = df[df['actor1name'] == None]
    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1  where $t1.actor1name is NULL"
    self.matchSnipped(actual, expected)  

  def test_Ne(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] != 468189636]
    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1  where $t1.globaleventid <> 468189636"

    self.matchSnipped(actual, expected)


  def test_NeNone(self):
    df = grizzly.read_table("events") 
    df = df[df['actor1name'] != None]
    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1  where $t1.actor1name is not NULL"
    self.matchSnipped(actual, expected)  

  def test_Lt(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] < 468189636]
    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1  where $t1.globaleventid < 468189636"
    self.matchSnipped(actual, expected)

  def test_LtNone(self):
    df = grizzly.read_table("events") 
    df = df[df['actor1name'] < None]
    
    with self.assertRaises(ExpressionException):
      df.generateQuery()

    
    
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

  def test_shapeFull(self):
    df = grizzly.read_table("events") 

    (cols, rows) = df.shape

    self.assertEqual(cols, 58)
    self.assertEqual(rows, 30354)

  def test_shapeGrp(self):
    df = grizzly.read_table("events")
    g = df.groupby(["theyear","actor1name"])
    a = g.agg(col="actor2name", aggType=AggregateType.COUNT,alias="cnt_actor")
    f = a.filter(a["cnt_actor"] > 2)

    (cols, rows) = f.shape

    self.assertEqual(cols, 3) # 2 grouping + 1 aggr
    self.assertEqual(rows, 879)

  def test_Len(self):
    df = grizzly.read_table("events") 
    l = len(df)

    self.assertEqual(l, 30354)

  def test_LenJoin(self):
    df1 = grizzly.read_table("t1")
    df2 = grizzly.read_table("t2")
    
    j  = df1.join(df2, on = (df1.actor1name == df2.actor2name) | (df1["actor1countrycode"] <= df2["actor2countrycode"]), how="left outer")
    cnt = len(j)
    self.assertEqual(cnt, 9899259)

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

  def test_tail(self):
    df = grizzly.read_table("events")
    df = df.sort_values("globaleventid")
    tl = df.tail(10)
    print(tl)

    self.assertEqual(len(tl), 10)

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

  # def test_toString(self):
  #   df = grizzly.read_table("events") 

  #   df = df[df['globaleventid'] == 467268277]
  #   df = df[["actor1name","actor2name", "globaleventid","sourceurl"]]

  #   strDF = str(df)
  #   splt = strDF.split("\n")

  #   rows = df.count()
  #   dfLen = len(splt)
  #   rowsLen = rows+ 1 # column names

  #   self.assertEqual(dfLen, rowsLen) 

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

    expected = f"""create or replace function myfunc(a int) returns varchar(1024) language plpython3u as 'return a+"_grizzly"' parallel safe;{sql}"""

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
    expected = "select * from (select * from events $t0) $t1 natural join (select * from events $t2) $t3"
    self.matchSnipped(actual, expected)

  def test_limitgen(self):
    df = grizzly.read_table("events") 
    df = df[["globaleventid","actor1name"]]
    df = df.limit(10)

    expected = "select $t2.* from (select $t1.globaleventid, $t1.actor1name FROM (select * from events $t0) $t1) $t2 limit 10"
    actual = df.generateQuery()

    self.matchSnipped(actual, expected)

  def test_limitExec(self):
    n = 10

    df = grizzly.read_table("events") 
    df = df[["globaleventid","actor1name"]]
    df = df.limit(n)
    
    data = df.collect()

    self.assertEqual(len(data), n)

  def test_sliceExec(self):
    df = grizzly.read_table("events")
    df = df[5:10]
    data = df.collect()

    self.assertEqual(len(data),10)

  def test_sliceGen(self):
    df = grizzly.read_table("events") 
    df = df[["globaleventid","actor1name"]]
    df = df[5:10]

    expected = "select $t2.* from (select $t1.globaleventid, $t1.actor1name FROM (select * from events $t0) $t1) $t2 limit 10 offset 5"
    actual = df.generateQuery()

    self.matchSnipped(actual, expected)

  def test_orderingdefault(self):
    df = grizzly.read_table("events") 
    df = df[["globaleventid","actor1name"]]
    df = df.sort_values(by = "globaleventid")

    actual = df.generateQuery()

    expected = "select * from (select $t1.globaleventid, $t1.actor1name from (select * from events $t0) $t1) $t2 order by $t2.globaleventid asc"

    self.matchSnipped(actual, expected)

  def test_orderingDESC(self):
    df = grizzly.read_table("events") 
    df = df[["globaleventid","actor1name"]]
    df = df.sort_values(by = "globaleventid", ascending=False)

    actual = df.generateQuery()

    expected = "select * from (select $t1.globaleventid, $t1.actor1name from (select * from events $t0) $t1) $t2 order by $t2.globaleventid desc"

    self.matchSnipped(actual, expected)

  def test_orderingMulti(self):
    df = grizzly.read_table("events") 
    df = df[["globaleventid","actor1name"]]
    df = df.sort_values(by = ["globaleventid","actor1name"])

    actual = df.generateQuery()

    expected = "select * from (select $t1.globaleventid, $t1.actor1name from (select * from events $t0) $t1) $t2 order by $t2.globaleventid, $t2.actor1name asc"

    self.matchSnipped(actual, expected)

  def test_orderingMultiDESC(self):
    df = grizzly.read_table("events") 
    df = df[["globaleventid","actor1name"]]
    df = df.sort_values(by = ["globaleventid","actor1name"],ascending=False)

    actual = df.generateQuery()

    expected = "select * from (select $t1.globaleventid, $t1.actor1name from (select * from events $t0) $t1) $t2 order by $t2.globaleventid, $t2.actor1name desc"

    self.matchSnipped(actual, expected)

  def test_orderingMultiSingleRef(self):
    df = grizzly.read_table("events") 
    df = df[["globaleventid","actor1name"]]
    df = df.sort_values(by = df.globaleventid)

    actual = df.generateQuery()

    expected = "select * from (select $t1.globaleventid, $t1.actor1name from (select * from events $t0) $t1) $t2 order by $t2.globaleventid asc"

    self.matchSnipped(actual, expected)

  def test_orderingMultiRef(self):
    df = grizzly.read_table("events") 
    df = df[["globaleventid","actor1name"]]
    df = df.sort_values(by = [df.globaleventid, df["actor1name"]])

    actual = df.generateQuery()

    expected = "select * from (select $t1.globaleventid, $t1.actor1name from (select * from events $t0) $t1) $t2 order by $t2.globaleventid, $t2.actor1name asc"

    self.matchSnipped(actual, expected)

  def test_iterate(self):
    df = grizzly.read_table("events")

    cnt = 0
    for _ in df:
      cnt += 1

    expected = df.count()

    self.assertEqual(cnt, expected)

  def test_iterrows(self):
    df = grizzly.read_table("events")
    df = df[[df.actor1name, df.actor2name]]
    df = df[100:10]

    n = 0
    for num, row in df.iterrows():
      self.assertEqual(num, n, "row num")
      self.assertEqual(len(row), 2)
      n += 1

    self.assertEqual(n, 10, "total number") # will be increased one more time in last iteration

  def test_itertuples(self):
    df = grizzly.read_table("events")
    df = df[[df.actor1name, df.actor2name]]
    df = df[100:10]

    r = re.compile(r"Grizzly\(actor1name=.+, actor2name=.+\)")

    n = 0
    for tup in df.itertuples():
      s = str(tup)
      self.assertRegex(s, r)
      n += 1

    self.assertEqual(n, 10, "total number") # will be increased one more time in last iteration

  def test_items(self):
    df = grizzly.read_table("events")
    df = df[[df.actor1name, df.actor2name]]
    df = df[100:10]

    i = 0
    names = ["actor1name", "actor2name"]
    for item in df.items():
      self.assertEqual(item[0], names[i]) # name column
      self.assertEqual(len(item[1]),10)
      i += 1

    self.assertEqual(i, 2) # two columns

  def test_at(self):
    df = grizzly.read_table("events",index="globaleventid")
    res = df.at[467268277,'actor1name']

    self.assertEqual(len(res), 1)
    self.assertEqual(res[0], 'AFRICA')

  def test_atColOnly(self):
    df = grizzly.read_table("events",index="globaleventid")
    res = df.at[df.actor1name]

    self.assertEqual(len(res), 1)
    # self.assertEqual(len(res[0]), 1)

  def test_locInt(self):
    df = grizzly.read_table("events", index="globaleventid")
    res = df.loc[467268277].collect()

    self.assertEqual(len(res), 1)
    self.assertEqual(len(res[0]), 58)


  def test_locIntNoIndex(self):
    df = grizzly.read_table("events", index=None)
 
    with self.assertRaises(ValueError):
      df.loc[467268277].collect()


  def test_locListGen(self):
    df = grizzly.read_table("events", index="globaleventid")
    df = df.loc[[467268277,477265011]]

    actual = df.generateQuery()
    expected = "select * from (select * from events $t0) $t1 WHERE $t1.globaleventid in (467268277,477265011)"    

    self.matchSnipped(actual, expected)

  def test_locList(self):
    df = grizzly.read_table("events", index="globaleventid")
    df = df.loc[[467268277,477265011]]

    res = df.collect()    

    self.assertEqual(len(res), 2)
    self.assertEqual(len(res[0]), 58)
    self.assertEqual(len(res[1]), 58)

  def test_colAggmin(self):
    df = grizzly.read_table("events")
    minTone1 = df["avgtone"].min()
    minTone2 = df.min("avgtone")

    self.assertEqual(minTone1, minTone2,"col.min vs min(col)")

  def test_colAggMax(self):
    df = grizzly.read_table("events")
    maxTone1 = df["avgtone"].max()
    maxTone2 = df.max("avgtone")

    self.assertEqual(maxTone1, maxTone2,"col.max vs max(col)")

  def test_colAggSum(self):
    df = grizzly.read_table("events")
    sumTone1 = df["avgtone"].sum()
    sumTone2 = df.sum("avgtone")

    self.assertEqual(sumTone1, sumTone2,"col.sum vs sum(col)")

  def test_colAggCount(self):
    df = grizzly.read_table("events")
    countTone1 = df["avgtone"].count()
    countTone2 = df.count("avgtone")

    self.assertEqual(countTone1, countTone2,"col.count vs count(col)")

  def test_colAggMean(self):
    df = grizzly.read_table("events")
    meanTone1 = df["avgtone"].mean()
    meanTone2 = df.mean("avgtone")

    self.assertEqual(meanTone1, meanTone2,"col.mean vs mean(col)")

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
    from grizzly.generator import GrizzlyGenerator
    oldGen = GrizzlyGenerator._backend.queryGenerator

    newGen = SQLGenerator("vector")
    GrizzlyGenerator._backend.queryGenerator = newGen

    try:
      df = grizzly.read_external_files("filename.csv", ["a:int, b:str, c:float"], False, format="csv")
      actual = df.generateQuery()
      expected = "DROP TABLE IF EXISTS temp_ext_table$t0; " \
                "CREATE EXTERNAL TABLE temp_ext_table$t0(a int, b VARCHAR(1024), c float) " \
                "USING SPARK WITH REFERENCE='filename.csv', FORMAT='csv', OPTIONS=('delimiter'='|','header'='false','schema'='a int, b VARCHAR(1024), c float') " \
                "SELECT * FROM temp_ext_table$t0 $t0"
      self.matchSnipped(actual, expected)

      df = grizzly.read_external_files("filename.csv", ["a:int, b:str, c:float"], True, format="csv")
      actual = df.generateQuery()
      expected = "DROP TABLE IF EXISTS temp_ext_table$t0; " \
                "CREATE EXTERNAL TABLE temp_ext_table$t0(a int, b VARCHAR(1024), c float) " \
                "USING SPARK WITH REFERENCE='filename.csv', FORMAT='csv', OPTIONS=('delimiter'='|') " \
                "SELECT * FROM temp_ext_table$t0 $t0"
      self.matchSnipped(actual, expected)

      df = grizzly.read_external_files("filename.csv", ["a:int, b:str, c:float"], True, ',', format="csv")
      actual = df.generateQuery()
      expected = "DROP TABLE IF EXISTS temp_ext_table$t0; " \
                "CREATE EXTERNAL TABLE temp_ext_table$t0(a int, b VARCHAR(1024), c float) " \
                "USING SPARK WITH REFERENCE='filename.csv', FORMAT='csv', OPTIONS=('delimiter'=',') " \
                "SELECT * FROM temp_ext_table$t0 $t0"
      self.matchSnipped(actual, expected)

      df = grizzly.read_external_files("filename.csv", ["a:int, b:str, c:float"], True, ',', format="csv")
      actual = df.generateQuery()
      expected = "DROP TABLE IF EXISTS temp_ext_table$t0; " \
                "CREATE EXTERNAL TABLE temp_ext_table$t0(a int, b VARCHAR(1024), c float) " \
                "USING SPARK WITH REFERENCE='filename.csv', FORMAT='csv', OPTIONS=('delimiter'=',') " \
                "SELECT * FROM temp_ext_table$t0 $t0"
      self.matchSnipped(actual, expected)
    finally:
      GrizzlyGenerator._backend.queryGenerator = oldGen

  def test_computedColML(self):

    from grizzly.generator import GrizzlyGenerator
    oldGen = GrizzlyGenerator._backend.queryGenerator

    newGen = SQLGenerator("postgresql")
    GrizzlyGenerator._backend.queryGenerator = newGen

    def input_to_tensor(input:str):
      return input

    def tensor_to_output(tensor) -> str:
      return "positiv"

    try:
      onnx_path = "/var/lib/postgresql/roberta-sequence-classification.onnx"
      df = grizzly.read_table("reviews_SIZE")
      df["sentiment"] = df["review"].apply_onnx_model(onnx_path, input_to_tensor, tensor_to_output)
      df = df.groupby(["sentiment"]).count("review")
      
      # df.show(pretty = True)

      actual = df.generateQuery()
      expected = """CREATE OR REPLACE FUNCTION apply(input varchar(1024)) RETURNS varchar(1024) LANGUAGE plpython3u AS 'import onnxruntime
import random
def apply(input: str) -> str:
      def input_to_tensor(input:str):
      return input


      def tensor_to_output(tensor) -> str:
      return "positiv"


  def apply_model(input):
    if not hasattr(random, "onnx_session"):
        random.onnx_session = onnxruntime.InferenceSession("/var/lib/postgresql/roberta-sequence-classification.onnx")
    inputs = input_to_tensor(input)
    ret = random.onnx_session.run(None, inputs)
    return(tensor_to_output(ret))
  return apply_model(input)
return apply(input)
' parallel safe; SELECT sentiment, count($t0.review) FROM (SELECT *, apply($t2.review) as sentiment FROM reviews_SIZE $t2) $t0 GROUP BY sentiment"""

      self.matchSnipped(actual, expected)
    finally:
      GrizzlyGenerator._backend.queryGenerator = oldGen


if __name__ == "__main__":
    unittest.main()

