#!/bin/bash

python3 roberta_save_pretrained.py 

service postgresql start
echo "alter user postgres password 'password123';" | psql
echo "drop database if exists movies;" | psql
echo "create database movies;" | psql
echo "CREATE EXTENSION IF NOT EXISTS plpython3u;" | psql movies
echo "create table review(URL text, review text); " | psql movies
echo "COPY review(URL, review) from '/var/lib/postgresql/grizzly/imdb/data.csv' delimiter '|' csv;"| psql movies
echo "create table review_10 as select * from review limit 10;" | psql movies
echo "create table review_50 as select * from review limit 50;" | psql movies
echo "create table review_100 as select * from review limit 100;" | psql movies
echo "create table review_500 as select * from review limit 500;" | psql movies
echo "create table review_1000 as select * from review limit 1000;" | psql movies
