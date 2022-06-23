# Grizzly

[![Testing](https://dbgit.prakinf.tu-ilmenau.de/code/grizzly/badges/master/pipeline.svg)](https://dbgit.prakinf.tu-ilmenau.de/code/grizzly/commits/master)
[![coverage report](https://dbgit.prakinf.tu-ilmenau.de/code/grizzly/badges/master/coverage.svg)](https://dbgit.prakinf.tu-ilmenau.de/code/grizzly/commits/master)

Grizzly is a transpiler from a Python-API to SQL to move computations from the client into a database system.

Grizzly implements its own `DataFrame` structure that tracks operations, like projection, filter, joins, ...
Only when the result of the sequence of operations is needed, a SQL string is produced, resembling all those operations, and sent to a DBMS.
This way, you don't have to care about Out-of-Memory problems, un-optimized queries, and high CPU load.

## Publications
We presented the idea as well as key concepts at several conferences:

 - Stefan Hagedorn: [**When sweet and cute isn't enough anymore: Solving scalability issues in Python Pandas with Grizzly.**](http://cidrdb.org/cidr2020/gongshow2020/gongshow/abstracts/cidr2020_abstract76.pdf), *CIDR 2020*
 - Stefan Hagedorn, Steffen Kläbe, Kai-Uwe Sattler: [**Putting Pandas in a Box**](http://cidrdb.org/cidr2021/papers/cidr2021_paper07.pdf), *CIDR 2021*
   - [Presentation on Youtube](https://www.youtube.com/watch?v=8zUszpr0300)
 - Steffen Kläbe, Stefan Hagedorn: [**When Bears get Machine Support: Applying Machine Learning Models to Scalable DataFrames with Grizzly**](https://dl.gi.de/bitstream/handle/20.500.12116/35793/A2-4.pdf), *BTW 2021*
 - Stefan Hagedorn, Steffen Kläbe, Kai-Uwe Sattler: [**Conquering a Panda’s weaker self - Fighting laziness with laziness**](https://edbt2021proceedings.github.io/docs/p174.pdf), *EDBT 2021*, Demo Paper
   - [Presentation on Youtube](https://www.youtube.com/embed/nBvUPlU_NOU)
 - Steffen Kläbe, Robert DeSantis, Stefan Hagedorn, Kai-Uwe Sattler: [**Accelerating Python UDFs in Vectorized Query Execution**](http://cidrdb.org/cidr2022/papers/p33-klaebe.pdf), *CIDR 2022*
   - [Presentation on Youtube](https://www.youtube.com/watch?v=FLatSmSGkk8)


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
- [PyYAML](https://pypi.org/project/PyYAML/) for support of vendor-specific query templates
- [antlr4-python3-runtime 4.9.3](https://pypi.org/project/antlr4-python3-runtime/4.9.3/) for compiling Python UDFs to prozedual sql

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

The parameter to `SQLGenerator` defines the SQL dialect of the underlying database system. We store vendor-specific code in a configuration file `grizzly.yml`. The dialect is only needed for `limit` operation which some SQL engines implement as `LIMIT` whereas others have `TOP`. Also UDFs (see below) require system-specific code.

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

A column can also be referenced using the dot notation, e.g. `df.actor1name`.


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
FROM (SELECT * FROM t1 _t0) _t1  
    left outer JOIN (SELECT * FROM t2 _t2) _t3 ON _t1.actor1name = _t3.actor2name or _t1.actor1countrycode <= _t3.actor2countrycode
```

### Grouping & Aggregation

You can also group the data on multiple columns and compute an aggregate over the groups using `agg`:

```python
from grizzly.aggregates import AggregateType
df = grizzly.read_table("events")
g = df.groupby(["year","actor1name"])

a = g.agg(col="actor2name", aggType=AggregateTyoe.COUNT)
```

Here, `a` represents a DataFrame with three columns: `year`, `monthyear` and the `count` value. In the above example, `a.generateQuery()` will give

```sql
SELECT _t0.year, _t0.actor1name, count(_t0.actor2name)
FROM events _t0 
GROUP BY _t0.year, _t0.actor1name
```

If no aggregation function and projection is used, only the grouping columns are selected upon query generation.

You can apply aggregation functions on non-grouped `DataFrame`s of course. In this case the aggregates will be computed for the whole content. For example, `g.count()` immediately runs the following query and returns the scalar value
```sql
SELECT count(*) FROM (
    SELECT _t1.year, _t1.actor1name
    FROM (SELECT * FROM events _t0) _t1
    GROUP BY _t1.year, _t1.actor1name
    ) _t2
```

A `df.count()` (i.e. before the grouping) for the above piece of code will return the single scalar value with the number of records in `df` (22225).
The query executed for this is:

```sql
SELECT count(*)
FROM events
```

Grizzly supports predefined aggregations, defined in the `AggregateType` enum: `MIN`, `MAX`, `MEAN`, `SUM`, `COUNT`. 
Other functions can be applied by passing the name of the functions as a string instead of the `ENUM` value.

### User Defined Functions & Computed Columns
Grizzly allows to apply almost any function defined in Python on your data. Currently, we support scala functions only.

```Python
def myfunc(a: int) -> str:
      return a+"_grizzly"
    
df = grizzly.read_table("events")  # load table
df = df[df.globaleventid == 467268277] # filter it
```

Apply function with Python code on dbms (supported by PostgreSQL, Actian Vector and MonetDB)
```Python
df["newid"] = df["globaleventid"].map(myfunc) # apply myfunc
```

Apply translated function with procedural SQL code (Oracle and PostgreSQL supported)
```Python
df["newid"] = df["globaleventid"].map(myfunc, lang='sql', fallback=True) # apply myfunc
```

The `lang` parameter defines whether the function is executed with Python code or the code is translated with the integrated `udfcompiler` module to a procedural language. The `fallback` parameter allows to apply the function with Python code or locally to a `Pandas DataFrame` if compilation errors occur.

In the example above, the function `myfunc` is applied to all entries in the `globaleventid` column and the result is stored in a new column `newid`. 

This way new columns can be added to the result. The value of a computed column can be any expression.

```Python
df["newcol"] = df.theyear + df.monthyear
```

### Apply Machine Learning Models
Using the UDF mechanism described above, we enable users to easily apply their pre-trained models to their data inside the DB. 

For ONNX models, users only need to specify the path to the model file (must be availble for the database engine) as well as two conversion functions: 
  - first functions converts the tuple into the format expected by the model
  - the second function converts the output of the model into a format the DB (and user) can handle. 

The [ONNX model zoo](https://github.com/onnx/models) provides a rich set of models with the according conversion functions.

```Python
def input_to_model(a: str):
        ...

def model_to_output(a) -> str:
        ...

df = grizzly.read_table('tab') # load table
# apply model to every value in column 'col'
# using provided input and output conversion functions
# store model output in computed column 'classification'
df['classification'] = df['col'].apply_model("/path/to/model", input_to_model, model_to_output)
# group by e.g. predicted classes
df = df.groupby(['classification']).count()
df.show()
```

### SQL

You can inspect the produced query string (in this case SQL) with `generateQuery()`:

```Python
print(df.generateQuery())
```


## Supported operations

- filter/selection
- projection
- join
- group by
- aggregation functions: min, max, mean (avg), count, sum
- user defined functions
- apply TensorFlow, PyTorch, ONNX models

## Limitations

 - Our DataFrame implementation is not yet fully compatibile with Pandas, but we are working on it.
 - Grizzly is under active development and things might change.
 - There are certainly some bugs. Probably with complex queries.


# Vision

Grizzly is a research project. We aim at bringing data-intensive operations back into the database system. Our plan is to extend Grizzly in the following ways - some of them are inspired by our other projects:

  - Support for heterogeneous data sources:
    - Combine data from different sources (relational DB, file, HDFS, NoSQL) in one program/query (i.e. Polystores, federated query processing)
    - automatically import external data when neccessary
  - Add spatial operations
  - Stream processing operations
  - Code generation
    - Procude native code from the Python API
 
