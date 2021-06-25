ALTER TABLE orders   ADD CONSTRAINT pk_orders   PRIMARY KEY (o_orderkey); 
-- ALTER TABLE partsupp ADD CONSTRAINT pk_partsupp PRIMARY KEY (ps_partkey, ps_suppkey);
ALTER TABLE part     ADD CONSTRAINT pk_part     PRIMARY KEY (p_partkey); 
ALTER TABLE customer ADD CONSTRAINT pk_customer PRIMARY KEY (c_custkey); 
ALTER TABLE supplier ADD CONSTRAINT pk_supplier PRIMARY KEY (s_suppkey);
ALTER TABLE nation   ADD CONSTRAINT pk_nation   PRIMARY KEY (n_nationkey);
ALTER TABLE region   ADD CONSTRAINT pk_region   PRIMARY KEY (r_regionkey);
ALTER TABLE lineitem ADD CONSTRAINT pk_lineitem PRIMARY KEY (l_orderkey, l_linenumber); 

