#!/bin/bash
if [ ! -f /var/lib/postgresql/tpch-dbgen/orders.tbl ]; then
	cd /var/lib/postgresql/tpch-dbgen
	./dbgen -s 100 -T O -f
	cd ~/grizzly
	# Drop trailing delimiter. Postgres has option to ignore last column.
	sed -i 's/.$//' /var/lib/postgresql/tpch-dbgen/orders.tbl
fi

if [ ! -f /var/lib/postgresql/tpch-dbgen/customer.tbl ]; then
        cd /var/lib/postgresql/tpch-dbgen
        ./dbgen -s 100 -T c -f
        cd ~/grizzly
        # Drop trailing delimiter. Postgres has option to ignore last column.
        sed -i 's/.$//' /var/lib/postgresql/tpch-dbgen/customer.tbl
fi


# Files for the csv_access_experiment
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 8500000 > /var/lib/postgresql/tpch-dbgen/orders_8500000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 17000000 > /var/lib/postgresql/tpch-dbgen/orders_17000000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 25500000 > /var/lib/postgresql/tpch-dbgen/orders_25500000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 34000000 > /var/lib/postgresql/tpch-dbgen/orders_34000000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 42500000 > /var/lib/postgresql/tpch-dbgen/orders_42500000.tbl

# Files for the external join experiment
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 100000 > /var/lib/postgresql/tpch-dbgen/orders_100000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 500000 > /var/lib/postgresql/tpch-dbgen/orders_500000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 1000000 > /var/lib/postgresql/tpch-dbgen/orders_1000000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 1500000 > /var/lib/postgresql/tpch-dbgen/orders_1500000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 2000000 > /var/lib/postgresql/tpch-dbgen/orders_2000000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 2500000 > /var/lib/postgresql/tpch-dbgen/orders_2500000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 3000000 > /var/lib/postgresql/tpch-dbgen/orders_3000000.tbl

service postgresql start
echo "alter user postgres password 'password123';" | psql
echo "drop database if exists tpch;" | psql
echo "create database tpch;" | psql
echo "CREATE EXTENSION IF NOT EXISTS file_fdw;" | psql tpch
echo "CREATE TABLE orders (
        o_orderkey BIGINT NOT NULL,
        o_custkey INTEGER NOT NULL,
        o_orderstatus CHAR(1) NOT NULL,
        o_totalprice NUMERIC NOT NULL,
        o_orderdate DATE NOT NULL,
        o_orderpriority CHAR(15) NOT NULL,
        o_clerk CHAR(15) NOT NULL,
        o_shippriority INTEGER NOT NULL,
        o_comment VARCHAR(79) NOT NULL
); " | psql tpch
echo "CREATE TABLE customer (
        c_custkey INTEGER NOT NULL,
        c_name VARCHAR(25) NOT NULL,
        c_address VARCHAR(40) NOT NULL,
        c_nationkey INTEGER NOT NULL,
        c_phone CHAR(15) NOT NULL,
        c_acctbal NUMERIC NOT NULL,
        c_mktsegment CHAR(10) NOT NULL,
        c_comment VARCHAR(117) NOT NULL
);" | psql tpch
echo "COPY orders from '/var/lib/postgresql/tpch-dbgen/orders.tbl' delimiter '|' csv;"| psql tpch
echo "COPY customer from '/var/lib/postgresql/tpch-dbgen/customer.tbl' delimiter '|' csv;"| psql tpch
echo "create table orders_8500000 as select * from orders limit 8500000;" | psql tpch
echo "create table orders_17000000 as select * from orders limit 17000000;" | psql tpch
echo "create table orders_25500000 as select * from orders limit 25500000;" | psql tpch
echo "create table orders_34000000 as select * from orders limit 34000000;" | psql tpch
echo "create table orders_42500000 as select * from orders limit 42500000;" | psql tpch
