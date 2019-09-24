import connection
import grizzly

from codematcher import CodeMatcher
import unittest
import sqlite3


class DataFrameTest(CodeMatcher):

  def setUp(self):
    # ("sqlite:///grizzly.db")
    connection.Connection.db = sqlite3.connect("grizzly.db")

  def tearDown(self):
    connection.Connection.db.close()

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

    self.assertEqual(len(strDF), rows + 3) # column names + top rule + bottom rule





if __name__ == "__main__":
    unittest.main()