#!/bin/bash
if [ ! -f /var/lib/postgresql/tpch-dbgen/orders.tbl ]; then
	cd /var/lib/postgresql/tpch-dbgen
	./dbgen -s 100 -T O -f
	cd ~/grizzly
	# Drop trailing delimiter. Postgres has option to ignore last column.
	sed -i 's/.$//' /var/lib/postgresql/tpch-dbgen/orders.tbl
fi

head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 8500000 > /var/lib/postgresql/tpch-dbgen/orders_8500000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 17000000 > /var/lib/postgresql/tpch-dbgen/orders_17000000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 25500000 > /var/lib/postgresql/tpch-dbgen/orders_25500000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 34000000 > /var/lib/postgresql/tpch-dbgen/orders_34000000.tbl
head /var/lib/postgresql/tpch-dbgen/orders.tbl -n 42500000 > /var/lib/postgresql/tpch-dbgen/orders_42500000.tbl


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
echo "COPY orders from '/var/lib/postgresql/tpch-dbgen/orders.tbl' delimiter '|' csv;"| psql tpch
echo "create table orders_8500000 as select * from orders limit 8500000;" | psql tpch
echo "create table orders_17000000 as select * from orders limit 17000000;" | psql tpch
echo "create table orders_25500000 as select * from orders limit 25500000;" | psql tpch
echo "create table orders_34000000 as select * from orders limit 34000000;" | psql tpch
echo "create table orders_42500000 as select * from orders limit 42500000;" | psql tpch
