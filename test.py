import connection
import grizzly

import unittest
import sqlite3


class DataFrameTest(unittest.TestCase):

  def setUp(self):
    connection.Connection.init("sqlite:///grizzly.db")

    

  def test_selectStar(self):
    df = grizzly.read_table("miotest_0_01gb") 
    self.assertEqual(df.sql().lower().strip(), "select  * from miotest_0_01gb")

  def test_selectCountStar(self):
    df = grizzly.read_table("miotest_0_01gb")
    self.assertEqual(df.count(), 30354)


  def test_selectStarFilter(self):
    df = grizzly.read_table("miotest_0_01gb") 
    df = df[df['globaleventid'] == 468189636]

    self.assertEqual(df.sql().lower().strip(), "select  * from miotest_0_01gb   where miotest_0_01gb.globaleventid = 468189636")


  def test_selectStarFilterString(self):
    df = grizzly.read_table("miotest_0_01gb") 
    df = df[df['globaleventid'] == 'abc']

    self.assertEqual(df.sql().lower().strip(), "select  * from miotest_0_01gb   where miotest_0_01gb.globaleventid = 'abc'")

  def test_selectColumnWithFilter(self):
    df = grizzly.read_table("miotest_0_01gb") 
    df = df[df['globaleventid'] == 468189636]
    df = df['goldsteinscale']

    self.assertEqual(df.sql().lower().strip(), "select  goldsteinscale from miotest_0_01gb   where miotest_0_01gb.globaleventid = 468189636")

  def test_selectCountCol(self):
    df = grizzly.read_table("miotest_0_01gb")
    cnt = df.count('actor2name')
    self.assertGreater(cnt, 0)

  def test_selectStarGroupBy(self):
    df = grizzly.read_table("miotest_0_01gb") 
    df = df[df['globaleventid'] == '468189636']
    g = df.groupby(["year","monthyear"])

    self.assertEqual(g.sql().lower().strip(), "select  miotest_0_01gb.year, miotest_0_01gb.monthyear from miotest_0_01gb   where miotest_0_01gb.globaleventid = '468189636'  group by miotest_0_01gb.year, miotest_0_01gb.monthyear")

  def test_groupByWithAggTwice(self):
    df = grizzly.read_table("miotest_0_01gb") 
    df = df[df['globaleventid'] == 468189636]
    g = df.groupby(["year","monthyear"])

    a = g.count("actor2geo_type")

    self.assertEqual(a.sql().lower().strip(), "select  miotest_0_01gb.year, miotest_0_01gb.monthyear, count(actor2geo_type) from miotest_0_01gb   where miotest_0_01gb.globaleventid = 468189636  group by miotest_0_01gb.year, miotest_0_01gb.monthyear")


    m = g.mean("avgtone")
    self.assertEqual(m.sql().lower(), "select  miotest_0_01gb.year, miotest_0_01gb.monthyear, avg(avgtone) from miotest_0_01gb   where miotest_0_01gb.globaleventid = 468189636  group by miotest_0_01gb.year, miotest_0_01gb.monthyear")

  def test_joinTest(self):
    df = grizzly.read_table("miotest_0_01gb") 
    df = df[df['globaleventid'] == 470259271]

    df2 = grizzly.read_table("miotest_0_01gb")
    
    joined = df.join(other = df2, on=["globaleventid", "globaleventid"], how = "inner")

    self.assertGreater(joined.count(), 0)

  def test_Distinct(self):
    df = grizzly.read_table("miotest_0_01gb")
    self.assertEqual(df['isrootevent'].distinct().sql().lower().strip(), "select distinct isrootevent from miotest_0_01gb")

  def test_Distinct(self):
    df = grizzly.read_table("miotest_0_01gb")
    self.assertEqual(df[['y',"x"]].distinct().sql().lower().strip(), "select distinct y,x from miotest_0_01gb")
    # print(df[['y',"x"]].distinct().sql().lower().strip())

if __name__ == "__main__":
    unittest.main()