ALTER TABLE nation   ADD CONSTRAINT fk_regionkey   FOREIGN KEY (n_regionkey)           REFERENCES region   (r_regionkey);
ALTER TABLE supplier ADD CONSTRAINT fk_s_nationkey FOREIGN KEY (s_nationkey)           REFERENCES nation   (n_nationkey);
ALTER TABLE customer ADD CONSTRAINT fk_c_nationkey FOREIGN KEY (c_nationkey)           REFERENCES nation   (n_nationkey);
ALTER TABLE partsupp ADD CONSTRAINT fk_partkey     FOREIGN KEY (ps_partkey)            REFERENCES part     (p_partkey); 
ALTER TABLE partsupp ADD CONSTRAINT fk_suppkey     FOREIGN KEY (ps_suppkey)            REFERENCES supplier (s_suppkey);
ALTER TABLE orders   ADD CONSTRAINT fk_custkey     FOREIGN KEY (o_custkey)             REFERENCES customer (c_custkey);
ALTER TABLE lineitem ADD CONSTRAINT fk_orderkey    FOREIGN KEY (l_orderkey)            REFERENCES orders   (o_orderkey);
-- ALTER TABLE lineitem ADD CONSTRAINT fk_partsupp    FOREIGN KEY (l_partkey, l_suppkey)  REFERENCES partsupp (ps_partkey, ps_suppkey);
ALTER TABLE lineitem ADD CONSTRAINT fk_part        FOREIGN KEY (l_partkey)             REFERENCES part     (p_partkey);
ALTER TABLE lineitem ADD CONSTRAINT fk_supplier    FOREIGN KEY (l_suppkey)             REFERENCES supplier (s_suppkey);
