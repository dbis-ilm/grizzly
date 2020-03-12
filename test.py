import unittest
import sqlite3

import re

import grizzly
from grizzly.sqlgenerator import SQLGenerator
from grizzly.relationaldbexecutor import RelationalExecutor

class CodeMatcher(unittest.TestCase):
  

  def matchSnipped(self, snipped, template):
    res, mapping, expanded = self.doMatchSnipped(snipped.strip(), template.strip())
    if not res:
      mapstr = "with mapping:\n"
      for templ,tVar in mapping.items():
        mapstr += f"\t{templ} -> {tVar}\n"
      self.fail(f"Mismatch\nFound:    {snipped}\nExpanded:\t{expanded}\nExpected: {template}\n{mapstr}")

      

  def doMatchSnipped(self, snipped, template):
    replacements = {}
    pattern = re.compile("\$t[0-9]+")

    # pattern2 = re.compile("[A-Z][A-Z][A-Z][A-Z][A-Z]")
    pattern2 = re.compile("_t[0-9]+")

    positions = [p.start() for i,p in enumerate(pattern.finditer(template))]

    keys = pattern.findall(template)
    offset = 0

    for i,pos in enumerate(positions):
      if len(snipped) < pos + offset + 1:
        return False,replacements, ""

      match = pattern2.search(snipped, positions[i] + offset)
      if match:
        snip = match.group(0)
        replacements[keys[i]] = snip
        offset += max([0, len(snip) - len(keys[i])])

    s = template
    for k,v in replacements.items():
      s = s.replace(k,v)

    return snipped.replace(" ","").lower() == s.replace(" ","").lower(), replacements, s


class DataFrameTest(CodeMatcher):

  @classmethod
  def setUpClass(cls):
    c = sqlite3.connect("grizzly.db")
    grizzly.use(RelationalExecutor(c))

  @classmethod
  def tearDownClass(cls):
    grizzly.close()

  def test_groupby(self):
    df = grizzly.read_table("events")
    g = df.groupby(["year","actor1name"])
    a = g._gen_count("actor2name")
    
    expected = "select $t0.year, $t0.actor1name, count($t0.actor2name) from events $t0 group by $t0.year, $0.actor1name"
    actual = a

    self.matchSnipped(actual, expected)

  def test_New(self):
    df = grizzly.read_table("events")
    df = df["a"]
    df = df[df["a"] == 2]

    df2 = grizzly.read_table("events")
    df3 = df.join(df2,on=["a","a"])
    actualDF = df.generate()
    expectedDF = "select $t0.a from events $t0 where $t0.a = 2"

    self.matchSnipped(actualDF, expectedDF)

    actualDF3 = df3.generate()
    expectedDF3 = "select $t0.a from events $t0 inner join (select * from events $t1) $t2 on $t0.a = $t2.a where $t0.a = 2"

  def test_selectStar(self):
    df = grizzly.read_table("events") 
    actual = df.generate().lower().strip()
    expected = "select * from events $t0"
    self.matchSnipped(actual, expected)

  def test_selectCountStar(self):
    df = grizzly.read_table("events")
    self.assertEqual(df.count(), 30354)


  def test_selectStarFilter(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 468189636]

    actual = df.generate().lower().strip()
    expected = "select * from events $t0  where $t0.globaleventid = 468189636"

    self.matchSnipped(actual, expected)


  def test_selectStarFilterString(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 'abc']
    actual = df.generate().lower().strip()
    expected = "select * from events $t0  where $t0.globaleventid = 'abc'"

    self.matchSnipped(actual, expected)

  def test_selectColumnWithFilter(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 468189636]
    df = df['goldsteinscale']

    actual = df.generate().lower().strip()
    expected = "select $t0.goldsteinscale from events $t0 where $t0.globaleventid = 468189636"

    self.matchSnipped(actual, expected)

  def test_selectCountCol(self):
    df = grizzly.read_table("events")
    cnt = df.count('actor2name')
    self.assertGreater(cnt, 0)

  def test_selectStarGroupBy(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == '468189636']
    g = df.groupby(["year","monthyear"])

    actual = g.generate().lower().strip()
    expected = "select $t0.year, $t0.monthyear from events $t0 where $t0.globaleventid = '468189636' group by $t0.year, $t0.monthyear"

    self.matchSnipped(actual, expected)

  def test_groupByWithAggTwice(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 476829606]
    g = df.groupby(["year","monthyear"])

    a = g.count("actor2geo_type")
    
    gActual = g.generate()
    gExpected = "select $t0.year, $t0.monthyear from events $t0 where $t0.globaleventid = 476829606 group by $t0.year, $t0.monthyear"

    self.assertEqual(a,1)
    self.matchSnipped(gActual, gExpected)


    m = g.mean("avgtone")
    self.assertEqual(m, 0.909090909090911)

  def test_joinTest(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 470259271]

    df2 = grizzly.read_table("events")
    
    joined = df.join(other = df2, on=["globaleventid", "globaleventid"], how = "inner")

    actual = joined.generate()
    expected = "SELECT * FROM events $t1 inner join events $t2 ON $t1.globaleventid = $t2.globaleventid where $t1.globaleventid = 470259271"

    self.matchSnipped(actual, expected)

    # self.assertGreater(joined.count(), 0)

  def test_complexJoin(self):
    df1 = grizzly.read_table("t1")
    df2 = grizzly.read_table("t2")

    j = df1.join(df2, on = (df1['a'] == df2['b']) & (df1['c'] <= df2['d']), how="left outer")

    expected = "SELECT * FROM t1 $t0 LEFT OUTER JOIN t2 $t2 ON $t0.a = $t2.b AND $t0.c <= $t2.d".lower()
    
    actual = j.generate().lower()

    self.matchSnipped(actual, expected)

  def test_triJoin(self):
    df1 = grizzly.read_table("t1")
    df2 = grizzly.read_table("t2")
    df3 = grizzly.read_table("t3")
    df3 = df3[["b","d"]]
    j = df1.join(df2, on = (df1['a'] == df2['b']) & (df1['c'] <= df2['d']), how="left outer")
    
    j = j[[df1.m,df2.x]]
    
    j2 = j.join(df3, on = (j['m'] == df3['b']) & (j['x'] <= df3['d']), how="inner")

    actual = j2.generate()
    expected = "select $t1.m, $t2.x, $t4.b, $t4.d from t1 $t1 left outer join t2 $t2 on $t1.a = $t2.b and $t1.c <= $t2.d inner join (select $t3.b, $t3.d from t3 $t3) $t4 on $t1.m = $t4.b and $t1.x <= $t4.d"
    self.matchSnipped(actual, expected)


  def test_DistinctAll(self):
    df = grizzly.read_table("events")
    df = df.distinct()
    actual = df.generate().lower().strip()
    expected = "SELECT distinct * FROM events $t1".lower()
    self.matchSnipped(actual, expected)

  def test_DistinctOneCol(self):
    df = grizzly.read_table("events")
    df = df['isrootevent'].distinct()
    actual = df.generate().lower().strip()
    # print(actual)
    expected = "select distinct $t1.isrootevent from events $t1"
    
    self.matchSnipped(actual, expected)
    # self.assertEqual

  def test_DistinctTwoCols(self):
    df = grizzly.read_table("events")
    df = df[['y',"x"]].distinct()
    actual = df.generate().lower().strip()
    expected = "select distinct $t0.y, $t0.x from events $t0"
    self.matchSnipped(actual, expected)
    # print(df[['y',"x"]].distinct().sql().lower().strip())

  def test_Eq(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 468189636]
    actual = df.generate().lower().strip()
    expected = "select * from events $t0  where $t0.globaleventid = 468189636"
    self.matchSnipped(actual, expected)

  def test_Ne(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] != 468189636]
    actual = df.generate().lower().strip()
    expected = "select * from events $t0  where $t0.globaleventid <> 468189636"

    self.matchSnipped(actual, expected)

  def test_Lt(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] < 468189636]
    actual = df.generate().lower().strip()
    expected = "select * from events $t0  where $t0.globaleventid < 468189636"
    self.matchSnipped(actual, expected)

  def test_Le(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] <= 468189636]
    actual = df.generate().lower().strip()
    expected = "select * from events $t0  where $t0.globaleventid <= 468189636"

    self.matchSnipped(actual, expected)

  def test_Gt(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] > 468189636]
    actual = df.generate().lower().strip()
    expected = "select * from events $t0  where $t0.globaleventid > 468189636"

    self.matchSnipped(actual, expected)

  def test_Ge(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] >= 468189636]
    actual = df.generate().lower().strip()
    expected = "select * from events $t0  where $t0.globaleventid >= 468189636"
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

      df.show()

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

    dfLen = len(splt)
    rowsLen = rows+ 3

    self.assertEqual(dfLen, rowsLen) # column names + top rule + bottom rule


if __name__ == "__main__":
    unittest.main()