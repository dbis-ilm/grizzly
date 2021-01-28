# Grizzly

[![Testing](https://dbgit.prakinf.tu-ilmenau.de/code/grizzly/badges/master/pipeline.svg)](https://dbgit.prakinf.tu-ilmenau.de/code/grizzly/commits/master)
[![coverage report](https://dbgit.prakinf.tu-ilmenau.de/code/grizzly/badges/master/coverage.svg)](https://dbgit.prakinf.tu-ilmenau.de/code/grizzly/commits/master)

Grizzly is a transpiler from a Python-API to SQL to move computations from the client into a database system.

Grizzly implements its own `DataFrame` structure that tracks operations, like projection, filter, joins, ...
Only when the result of the sequence of operations is needed, a SQL string is produced, resembling all those operations, and sent to a DBMS.
This way, you don't have to care about Out-of-Memory problems, un-optimized queries, and high CPU load.

## Installation

Grizzly is available on PyPi: <https://pypi.org/project/grizzly-sql>

```python
pip3 install --user grizzly-sql
```

## Dependencies

Grizzly uses

- Python 3
- [SQLite3](https://docs.python.org/2/library/sqlite3.html) (currently for tests only)
- [BeautifulTable](https://github.com/pri22296/beautifultable) for pretty output

## Getting started

### Import

As with any Python module, just import it

```Python
import grizzly
```

### Connection

Connect to your database using an appropriate connection string. In order to load the shipped test database containing events from the [GDELT](https://www.gdeltproject.org/) project:

```python
import sqlite3
con = sqlite3.connect("grizzly.db")
```
Grizzly uses different classes for code generation and executing the produced query.
Currently, Grizzly includes a SQL code generator and execution wrapper for relational DBMS (more will follow).
In order to activate them, set:

```python
from grizzly.relationaldbexecutor import RelationalExecutor
from grizzly.sqlgenerator import SQLGenerator
grizzly.use(RelationalExecutor(con, SQLGenerator("sqlite")))
```

The `RelationalExecutor` constructor has a parameter for the code generator to use. By default this is a `grizzly.sqlgenerator.SQLGenerator`, but can be set to some own implementation.

Now, reference the table(s) you want to work with:

```python
df = grizzly.read_table("events")
```

Here, `df` is just a reference, it contains no data from your table.
To show its complete contents, use the `show` method:

```python
df.show(pretty=True)
```

This will print the table's content on the screen. Alternatively, you can convert the dataframe into a string using `str(df)`.

In order to collect the result of a query/program into a local list, use `df.collect(includeHeader=True)`

### Filter & Projection

Operations are similar to Pandas:

```python
df[df["globaleventid"] == 470747760] # filter
df = df[["actor1name","actor2name"]] #projection
```

### Joins

A `DataFrame` can be joined with another `DataFrame`:

```python
df1 = grizzly.read_table("t1")
df2 = grizzly.read_table("t2")

joined = df1.join(df2, on=["actor1name", "actor2name"], how="inner", comp='=')
```

In the `on` parameter, you specify the join columns. The first one is for the left input (`df1`), the second one for the right input (`df2`).
The `how` parameter is used to select the join type: `inner`, `left outer`, etc. This value is directly placed into the generated query, and thus depends on
the dialect of the underlying DBMS. An additional `comp` parameter lets you choose the comparison operator.

You sometimes want to join on multiple columns with different comparisons. For this, in Grizzly you define the expression as if it was for filters:

```python
df1 = grizzly.read_table("t1")
df2 = grizzly.read_table("t2")

j = df1.join(df2, on = (df1.actor1name == df2.actor2name) | (df1["actor1countrycode"] <= df2["actor2countrycode"]), how="left outer")
```

This results in the following SQL code:

```sql
SELECT * 
FROM t1 _t0 
    left outer JOIN t2 _t1 ON _t0.actor1name = _t1.actor2name or _t0.actor1countrycode <= _t1.actor2countrycode
```

### Grouping & Aggregation

You can also group the data on multiple columns and compute an aggregate over the groups using `agg`:

```python
from grizzly.aggregates import AggregateType
df = grizzly.read_table("events")
g = df.groupby(["year","actor1name"])

a = g.agg(col="actor2name", aggType=AggregateTyoe.COUNT)
```

Here, `a` represents a DataFrame with three columns: `year`, `monthyear` and the `count` value. In the above example, `a.generate()` will give

```sql
SELECT _t0.year, _t0.actor1name, count(_t0.actor2name)
FROM events _t0 
GROUP BY _t0.year, _t0.actor1name
```

If no aggregation function and projection is used, only the grouping columns are selected upon query generation.

You can apply aggregation functions on non-grouped `DataFrame`s of course. In this case the aggregates will be computed for the whole content. For example, `g.count()` immediately runs the following query and returns the scalar value
```sql
SELECT count(*) FROM (
    SELECT _t0.year, _t0.actor1name
    FROM events _t0 
    GROUP BY _t0.year, _t0.actor1name
    ) _t1
```

A `df.count()` (i.e. before the grouping) for the above piece of code will return the single scalar value with the number of records in `df` (22225).
The query executed for this is:

```sql
SELECT count(*)
FROM events
```

Note, currently Grizzly supports predefined aggregations only. They are defined as constants in the `AggregateType` class: `MIN`, `MAX`, `MEAN`, `SUM`, `COUNT`. 
We are working on adding support for (arbitrary) user-defined functions (see below).

### SQL

You can inspect the produced query string (in this case SQL) with `generate()`:

```python
print(df.generate())
```


## Supported operations

- filter/selection
- projection
- join
- group by
- aggregation functions: min, max, mean (avg), count, sum

## Limitations

 - Currently, only the few operations above are supported -- more is to come
 - Grizzly is under active development and things might change.
 - There are certainly some bugs. Probably with complex queries


# Vision

Grizzly is a research project. We aim at bringing data-intensive operations back into the database system. Our plan is to extend Grizzly in the following ways - some of them are inspired by our other projects:

  - Support for heterogeneous data sources:
    - Combine data from different sources (relational DB, file, HDFS, NoSQL) in one program/query (i.e. Polystores, federated query processing)
    - automatically import external data when neccessary
  - Add spatial operations
  - Stream processing operations
  - Code generation
    - Procude native code from the Python API
 