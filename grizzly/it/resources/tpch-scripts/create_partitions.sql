CREATE TABLE customer_0 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 0);
CREATE TABLE customer_1 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 1);
CREATE TABLE customer_2 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 2);
CREATE TABLE customer_3 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 3);
CREATE TABLE customer_4 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 4);
CREATE TABLE customer_5 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 5);
CREATE TABLE customer_6 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 6);
CREATE TABLE customer_7 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 7);
CREATE TABLE customer_8 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 8);
CREATE TABLE customer_9 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 9);
CREATE TABLE customer_10 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 10);
CREATE TABLE customer_11 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 11);
CREATE TABLE customer_12 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 12);
CREATE TABLE customer_13 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 13);
CREATE TABLE customer_14 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 14);
CREATE TABLE customer_15 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 15);
CREATE TABLE customer_16 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 16);
CREATE TABLE customer_17 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 17);
CREATE TABLE customer_18 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 18);
CREATE TABLE customer_19 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 19);
CREATE TABLE customer_20 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 20);
CREATE TABLE customer_21 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 21);
CREATE TABLE customer_22 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 22);
CREATE TABLE customer_23 PARTITION OF customer FOR VALUES WITH (MODULUS 24, REMAINDER 23);
CREATE TABLE part_0 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 0);
CREATE TABLE part_1 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 1);
CREATE TABLE part_2 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 2);
CREATE TABLE part_3 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 3);
CREATE TABLE part_4 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 4);
CREATE TABLE part_5 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 5);
CREATE TABLE part_6 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 6);
CREATE TABLE part_7 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 7);
CREATE TABLE part_8 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 8);
CREATE TABLE part_9 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 9);
CREATE TABLE part_10 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 10);
CREATE TABLE part_11 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 11);
CREATE TABLE part_12 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 12);
CREATE TABLE part_13 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 13);
CREATE TABLE part_14 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 14);
CREATE TABLE part_15 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 15);
CREATE TABLE part_16 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 16);
CREATE TABLE part_17 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 17);
CREATE TABLE part_18 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 18);
CREATE TABLE part_19 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 19);
CREATE TABLE part_20 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 20);
CREATE TABLE part_21 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 21);
CREATE TABLE part_22 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 22);
CREATE TABLE part_23 PARTITION OF part FOR VALUES WITH (MODULUS 24, REMAINDER 23);
CREATE TABLE partsupp_0 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 0);
CREATE TABLE partsupp_1 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 1);
CREATE TABLE partsupp_2 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 2);
CREATE TABLE partsupp_3 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 3);
CREATE TABLE partsupp_4 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 4);
CREATE TABLE partsupp_5 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 5);
CREATE TABLE partsupp_6 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 6);
CREATE TABLE partsupp_7 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 7);
CREATE TABLE partsupp_8 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 8);
CREATE TABLE partsupp_9 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 9);
CREATE TABLE partsupp_10 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 10);
CREATE TABLE partsupp_11 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 11);
CREATE TABLE partsupp_12 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 12);
CREATE TABLE partsupp_13 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 13);
CREATE TABLE partsupp_14 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 14);
CREATE TABLE partsupp_15 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 15);
CREATE TABLE partsupp_16 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 16);
CREATE TABLE partsupp_17 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 17);
CREATE TABLE partsupp_18 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 18);
CREATE TABLE partsupp_19 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 19);
CREATE TABLE partsupp_20 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 20);
CREATE TABLE partsupp_21 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 21);
CREATE TABLE partsupp_22 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 22);
CREATE TABLE partsupp_23 PARTITION OF partsupp FOR VALUES WITH (MODULUS 24, REMAINDER 23);
CREATE TABLE orders_0 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 0);
CREATE TABLE orders_1 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 1);
CREATE TABLE orders_2 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 2);
CREATE TABLE orders_3 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 3);
CREATE TABLE orders_4 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 4);
CREATE TABLE orders_5 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 5);
CREATE TABLE orders_6 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 6);
CREATE TABLE orders_7 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 7);
CREATE TABLE orders_8 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 8);
CREATE TABLE orders_9 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 9);
CREATE TABLE orders_10 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 10);
CREATE TABLE orders_11 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 11);
CREATE TABLE orders_12 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 12);
CREATE TABLE orders_13 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 13);
CREATE TABLE orders_14 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 14);
CREATE TABLE orders_15 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 15);
CREATE TABLE orders_16 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 16);
CREATE TABLE orders_17 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 17);
CREATE TABLE orders_18 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 18);
CREATE TABLE orders_19 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 19);
CREATE TABLE orders_20 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 20);
CREATE TABLE orders_21 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 21);
CREATE TABLE orders_22 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 22);
CREATE TABLE orders_23 PARTITION OF orders FOR VALUES WITH (MODULUS 24, REMAINDER 23);
CREATE TABLE lineitem_0 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 0);
CREATE TABLE lineitem_1 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 1);
CREATE TABLE lineitem_2 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 2);
CREATE TABLE lineitem_3 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 3);
CREATE TABLE lineitem_4 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 4);
CREATE TABLE lineitem_5 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 5);
CREATE TABLE lineitem_6 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 6);
CREATE TABLE lineitem_7 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 7);
CREATE TABLE lineitem_8 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 8);
CREATE TABLE lineitem_9 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 9);
CREATE TABLE lineitem_10 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 10);
CREATE TABLE lineitem_11 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 11);
CREATE TABLE lineitem_12 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 12);
CREATE TABLE lineitem_13 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 13);
CREATE TABLE lineitem_14 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 14);
CREATE TABLE lineitem_15 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 15);
CREATE TABLE lineitem_16 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 16);
CREATE TABLE lineitem_17 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 17);
CREATE TABLE lineitem_18 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 18);
CREATE TABLE lineitem_19 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 19);
CREATE TABLE lineitem_20 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 20);
CREATE TABLE lineitem_21 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 21);
CREATE TABLE lineitem_22 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 22);
CREATE TABLE lineitem_23 PARTITION OF lineitem FOR VALUES WITH (MODULUS 24, REMAINDER 23);
