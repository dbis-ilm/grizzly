--create index orders_idx on orders(o_orderdate);
create index lineitem_idx on lineitem(l_orderkey);
create index part_idx on part(p_partkey);
create index partsupp_idx on partsupp(ps_partkey);
create index region_idx on region(r_regionkey);
create index nation_idx on nation(n_regionkey);
create index customer_idx on customer(c_nationkey);
create index supplier_idx on supplier(s_nationkey);