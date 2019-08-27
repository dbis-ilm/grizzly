[![Testing](https://dbgit.prakinf.tu-ilmenau.de/code/grizzly/badges/master/pipeline.svg)](https://dbgit.prakinf.tu-ilmenau.de/code/grizzly/commits/master)
[![coverage report](https://dbgit.prakinf.tu-ilmenau.de/code/grizzly/badges/master/coverage.svg)](https://dbgit.prakinf.tu-ilmenau.de/code/grizzly/commits/master)

# Grizzly

Grizzly is a transpiler for a Pandas-like Python-API to SQL to move computations from the client into a database system.

Grizzly implements its own `DataFrame` structure that tracks operations, like projection, filter, joins, ...
Only when the result of the sequence of operations is needed, a SQL string is produced, resembling all those operations, and sent to a DBMS.
This way, you don't have to care about Out-of-Memory problems, un-optimized queries, and high CPU load.

## Dependencies
Grizzly uses
  - Python 3
  - [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
  - [SQLite3](https://docs.python.org/2/library/sqlite3.html) (currently for tests only)


## Getting started

### Connection
Connect to your database using an appropriate connection string:
```python 
    connection.Connection.init("sqlite:///grizzly.db")
```
Now, reference the table(s) you want to work with:
```python
    df = grizzly.read_table("events")
```
Here, `df` is just a reference, it contains no data from your table.
To show its contents, use the `show` method:
```python
    df.show()
```
This will print the table's content on the screen. 

### Filter & Projection
Operations are similar to Pandas:
```python
    df[df["id" == 42]] # filter
    df = df[["actor1","actor2"]]
```
### Joins

A `DataFrame` can be joined with another `DataFrame`:
```python
    df1 = grizzly.read_table("table1")
    df2 = grizzly.read_table("table2")

    joined = df1.join(df2, on=["joinCol1", "joinCol2"], how="inner", comp='=')
```
In the `on` parameter, you specify the join columns. The first one is for the left input (`df1`), the second one for the right input (`df2`).
The `how` parameter is used to select the join type: `inner`, `left outer`, etc. This value is directly placed into the generated query, and thus depends on 
the dialect of the underlying DBMS. An additional `comp` parameter lets you choose the comparison operator.

You sometimes want to join on multiple columns with different comparisons. For this, in Grizzly you define the expression as if it was for filters:
```python
    df1 = grizzly.read_table("t1")
    df2 = grizzly.read_table("t2")

    j = df1.join(df2, on = (df1['a'] == df2['b']) & (df1['c'] <= df2['d']), how="left outer")
```

This results in the following SQL code:
```sql    
    SELECT  * 
    FROM t1  
        LEFT OUTER JOIN (SELECT  * FROM t2   ) IOBRD 
        ON (t1.a = IOBRD.b) AND (t1.c <= IOBRD.d)
```
### Grouping & Aggregation

You can also group the data on multiple columns and compute an aggregate over the groups:
```python
    df = grizzly.read_table("events") 
    df = df[df['id'] == 42]
    g = df.groupby(["year","actor1"])

    a = g.count("actor2")
```
If no aggregation function is used an `show()` is called, only the grouping columns are selected.
You can apply aggregation functions on non-grouped `DataFrame`s of course. In this case the aggregates will be computed for the whole content.

Thus, `a.sql()` will give
```sql
    SELECT year, actor1, count(actor2) 
    FROM events
    WHERE id = 42
    GROUP BY year, actor1
```
, whereas `df.count()` (i.e. before the grouping) for the above piece of code will return the single scalar value with the number of records in `df`:
```sql
    SELECT count(*) 
    FROM events
    WHERE id = 42
```

### SQL

You can inspect the produced SQL string with `sql()`:
```python
    print(df.sql())
```
And the output will be 
```sql
    SELECT actor1, actor2
    FROM events
    WHERE id = 42
```

## Supported operations
  - filter/selection
  - projection
  - join
  - group by
  - aggregation functions