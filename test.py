import connection
import grizzly

import unittest

class DataFrameTest(unittest.TestCase):

  def setUp(self):
    connection.Connection.init("grizzlytest","grizzly","grizzly","cloud04",54322)    

  def test_selectStar(self):
    df = grizzly.read_table("gdeltevents20mio")
    self.assertEqual(df.sql().lower().strip(), "select * from gdeltevents20mio")

  def test_selectCountStar(self):
    df = grizzly.read_table("gdeltevents20mio")
    self.assertEqual(df.count(), 6544708)


  def test_selectStarFilter(self):
    df = grizzly.read_table("gdeltevents20mio") 
    df = df[df['globaleventid'] == 468189636]

    self.assertEqual(df.sql().lower().strip(), "select * from gdeltevents20mio   where gdeltevents20mio.globaleventid = 468189636")


  def test_selectStarFilterString(self):
    df = grizzly.read_table("gdeltevents20mio") 
    df = df[df['globaleventid'] == 'abc']

    self.assertEqual(df.sql().lower().strip(), "select * from gdeltevents20mio   where gdeltevents20mio.globaleventid = 'abc'")

  def test_selectColumnWithFilter(self):
    df = grizzly.read_table("gdeltevents20mio") 
    df = df[df['globaleventid'] == 468189636]
    df = df['goldsteinscale']

    self.assertEqual(df.sql().lower().strip(), "select goldsteinscale from gdeltevents20mio   where gdeltevents20mio.globaleventid = 468189636")

  def test_selectCountCol(self):
    df = grizzly.read_table("gdeltevents20mio")
    cnt = df.count('actor2name')
    self.assertGreater(cnt, 0)

  def test_selectStarGroupBy(self):
    df = grizzly.read_table("gdeltevents20mio") 
    df = df[df['globaleventid'] == '468189636']
    g = df.groupby(["year","monthyear"])

    self.assertEqual(g.sql().lower().strip(), "select gdeltevents20mio.year, gdeltevents20mio.monthyear from gdeltevents20mio   where gdeltevents20mio.globaleventid = '468189636'  group by gdeltevents20mio.year, gdeltevents20mio.monthyear")

  def test_groupByWithAggTwice(self):
    df = grizzly.read_table("gdeltevents20mio") 
    df = df[df['globaleventid'] == 468189636]
    g = df.groupby(["year","monthyear"])

    a = g.count("actor2geo_type")

    self.assertEqual(a.sql().lower().strip(), "select gdeltevents20mio.year, gdeltevents20mio.monthyear, count(actor2geo_type) from gdeltevents20mio   where gdeltevents20mio.globaleventid = 468189636  group by gdeltevents20mio.year, gdeltevents20mio.monthyear")


    m = g.mean("avgtone")
    self.assertEqual(m.sql().lower(), "select gdeltevents20mio.year, gdeltevents20mio.monthyear, avg(avgtone) from gdeltevents20mio   where gdeltevents20mio.globaleventid = 468189636  group by gdeltevents20mio.year, gdeltevents20mio.monthyear")

  def test_joinTest(self):
    df = grizzly.read_table("gdeltevents20mio") 
    df = df[df['globaleventid'] == 468189636]

    df2 = grizzly.read_table("miotest")
    
    joined = df.join(other = df2, on=["globaleventid", "globaleventid"], how = "inner")

    self.assertGreater(joined.count(), 0)

  def test_Fail(self):
    """
    Intendet to fail for test reasons
    """
    self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()