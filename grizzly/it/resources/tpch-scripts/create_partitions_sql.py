#!/usr/bin/python3

import sys

table = sys.argv[1]
num = int(sys.argv[2])

for i in range(0,num):
	sql = f"CREATE TABLE {table}_{i} PARTITION OF {table} FOR VALUES WITH (MODULUS {num}, REMAINDER {i});"
	print(sql)
