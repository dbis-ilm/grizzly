import unittest
import sqlite3

import re

import grizzly
from grizzly.connection import Connection 

class CodeMatcher(unittest.TestCase):
  

  def matchSnipped(self, snipped, template):
    res = self.doMatchSnipped(snipped.strip(), template.strip())

    if not res:
      self.fail(f"{snipped} does not match given template {template}")
      

  def doMatchSnipped(self, snipped, template):
    replacements = {}
    pattern = re.compile("\$.?[0-9]")

    pattern2 = re.compile("[A-Z][A-Z][A-Z][A-Z][A-Z]")

    positions = [p.start() - i for i,p in enumerate(pattern.finditer(template))]

    keys = pattern.findall(template)
    offset = 0

    for i,pos in enumerate(positions):
      if len(snipped) < pos + offset + 1:
        return False

      match = pattern2.search(snipped, positions[i] + offset)
      if match:
        snip = match.group(0)
        replacements[keys[i]] = snip
        offset += len(snip) - 1

    s = template
    for k,v in replacements.items():
      s = s.replace(k,v)

    return snipped == s


class DataFrameTest(CodeMatcher):

  def setUp(self):
    Connection.db = sqlite3.connect("grizzly.db")

  def tearDown(self):
    Connection.db.close()

  def test_selectStar(self):
    df = grizzly.read_table("events") 
    self.assertEqual(df.sql().lower().strip(), "select  * from events")

  def test_selectCountStar(self):
    df = grizzly.read_table("events")
    self.assertEqual(df.count(), 30354)


  def test_selectStarFilter(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 468189636]

    self.assertEqual(df.sql().lower().strip(), "select  * from events   where events.globaleventid = 468189636")


  def test_selectStarFilterString(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 'abc']

    self.assertEqual(df.sql().lower().strip(), "select  * from events   where events.globaleventid = 'abc'")

  def test_selectColumnWithFilter(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 468189636]
    df = df['goldsteinscale']

    self.assertEqual(df.sql().lower().strip(), "select  goldsteinscale from events   where events.globaleventid = 468189636")

  def test_selectCountCol(self):
    df = grizzly.read_table("events")
    cnt = df.count('actor2name')
    self.assertGreater(cnt, 0)

  def test_selectStarGroupBy(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == '468189636']
    g = df.groupby(["year","monthyear"])

    self.assertEqual(g.sql().lower().strip(), "select  events.year, events.monthyear from events   where events.globaleventid = '468189636'  group by events.year, events.monthyear")

  def test_groupByWithAggTwice(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 468189636]
    g = df.groupby(["year","monthyear"])

    a = g.count("actor2geo_type")

    self.assertEqual(a.sql().lower().strip(), "select  events.year, events.monthyear, count(actor2geo_type) from events   where events.globaleventid = 468189636  group by events.year, events.monthyear")


    m = g.mean("avgtone")
    self.assertEqual(m.sql().lower(), "select  events.year, events.monthyear, avg(avgtone) from events   where events.globaleventid = 468189636  group by events.year, events.monthyear")

  def test_joinTest(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 470259271]

    df2 = grizzly.read_table("events")
    
    joined = df.join(other = df2, on=["globaleventid", "globaleventid"], how = "inner")

    self.assertGreater(joined.count(), 0)

  def test_complexJoin(self):
    df1 = grizzly.read_table("t1")
    df2 = grizzly.read_table("t2")

    j = df1.join(df2, on = (df1['a'] == df2['b']) & (df1['c'] <= df2['d']), how="left outer")

    expected = "SELECT  * FROM t1  LEFT OUTER JOIN (SELECT  * FROM t2   ) $t1 ON (t1.a = $t1.b) AND (t1.c <= $t1.d)"
    
    self.matchSnipped(j.sql(), expected)

  def test_triJoin(self):
    df1 = grizzly.read_table("t1")
    df2 = grizzly.read_table("t2")
    df3 = grizzly.read_table("t3")
    df3 = df3[["b,d"]]
    j = df1.join(df2, on = (df1['a'] == df2['b']) & (df1['c'] <= df2['d']), how="left outer")
    
    j = j[["m","x"]]
    
    j2 = j.join(df3, on = (j['a'] == df3['b']) & (j['c'] <= df3['d']), how="inner")

    print(j2.sql())


  def test_Distinct(self):
    df = grizzly.read_table("events")
    self.assertEqual(df['isrootevent'].distinct().sql().lower().strip(), "select distinct isrootevent from events")

  def test_Distinct(self):
    df = grizzly.read_table("events")
    self.assertEqual(df[['y',"x"]].distinct().sql().lower().strip(), "select distinct y,x from events")
    # print(df[['y',"x"]].distinct().sql().lower().strip())

  def test_Eq(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] == 468189636]

    self.assertEqual(df.sql().lower().strip(), "select  * from events   where events.globaleventid = 468189636")

  def test_Ne(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] != 468189636]

    self.assertEqual(df.sql().lower().strip(), "select  * from events   where events.globaleventid <> 468189636")

  def test_Lt(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] < 468189636]

    self.assertEqual(df.sql().lower().strip(), "select  * from events   where events.globaleventid < 468189636")

  def test_Le(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] <= 468189636]

    self.assertEqual(df.sql().lower().strip(), "select  * from events   where events.globaleventid <= 468189636")

  def test_Gt(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] > 468189636]

    self.assertEqual(df.sql().lower().strip(), "select  * from events   where events.globaleventid > 468189636")

  def test_Ge(self):
    df = grizzly.read_table("events") 
    df = df[df['globaleventid'] >= 468189636]

    self.assertEqual(df.sql().lower().strip(), "select  * from events   where events.globaleventid >= 468189636")

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

    df = df[df['globaleventid'] <= 468189636 ]  #== 467268277
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

    strDF = str(df).split("\n")

    rows = df.count()

    dfLen = len(strDF)
    rowsLen = rows+ 3

    self.assertEqual(dfLen, rowsLen) # column names + top rule + bottom rule





if __name__ == "__main__":
    unittest.main()