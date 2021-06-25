CREATE TABLE region (
r_regionkey BIGINT NOT NULL,
r_name CHAR(25) NOT NULL,
r_comment VARCHAR(152) NOT NULL
);

CREATE TABLE nation (
n_nationkey BIGINT NOT NULL,
n_name CHAR(25) NOT NULL,
n_regionkey BIGINT NOT NULL,
n_comment VARCHAR(152) NOT NULL
);

CREATE TABLE supplier (
s_suppkey BIGINT NOT NULL,
s_name CHAR(25) NOT NULL,
s_address VARCHAR(40) NOT NULL,
s_nationkey BIGINT NOT NULL,
s_phone CHAR(15) NOT NULL,
s_acctbal DECIMAL(12,2) NOT NULL,
s_comment VARCHAR(101) NOT NULL
);

CREATE TABLE customer (
c_custkey BIGINT NOT NULL,
c_name VARCHAR(25) NOT NULL,
c_address VARCHAR(40) NOT NULL,
c_nationkey BIGINT NOT NULL,
c_phone CHAR(15) NOT NULL,
c_acctbal DECIMAL(12,2) NOT NULL,
c_mktsegment CHAR(10) NOT NULL,
c_comment VARCHAR(117) NOT NULL
);

CREATE TABLE part (
p_partkey BIGINT NOT NULL,
p_name VARCHAR(55) NOT NULL,
p_mfgr CHAR(25) NOT NULL,
p_brand CHAR(10) NOT NULL,
p_type VARCHAR(25) NOT NULL,
p_size INTEGER NOT NULL,
p_container CHAR(10) NOT NULL,
p_retailprice DECIMAL(12,2) NOT NULL,
p_comment VARCHAR(23) NOT NULL
);

CREATE TABLE partsupp (
ps_partkey BIGINT NOT NULL,
ps_suppkey BIGINT NOT NULL,
ps_availqty INTEGER NOT NULL,
ps_supplycost DECIMAL(12,2) NOT NULL,
ps_comment VARCHAR(199) NOT NULL
);

CREATE TABLE orders (
o_orderkey BIGINT NOT NULL,
o_custkey BIGINT NOT NULL,
o_orderstatus CHAR(1) NOT NULL,
o_totalprice DECIMAL(12,2) NOT NULL,
o_orderdate DATE NOT NULL,
o_orderpriority CHAR(15) NOT NULL,
o_clerk CHAR(15) NOT NULL,
o_shippriority INTEGER NOT NULL,
o_comment VARCHAR(79) NOT NULL
);

CREATE TABLE lineitem (
l_orderkey BIGINT NOT NULL,
l_partkey BIGINT NOT NULL,
l_suppkey BIGINT NOT NULL,
l_linenumber INTEGER NOT NULL,
l_quantity DECIMAL(12,2) NOT NULL,
l_extendedprice DECIMAL(12,2) NOT NULL,
l_discount DECIMAL(12,2) NOT NULL,
l_tax DECIMAL(12,2) NOT NULL,
l_returnflag CHAR(1) NOT NULL,
l_linestatus CHAR(1) NOT NULL,
l_shipdate DATE NOT NULL,
l_commitdate DATE NOT NULL,
l_receiptdate DATE NOT NULL,
l_shipinstruct CHAR(25) NOT NULL,
l_shipmode CHAR(10) NOT NULL,
l_comment VARCHAR(44) NOT NULL
);

