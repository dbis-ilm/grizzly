#/bin/bash

service postgresql start
echo "alter user postgres password 'password123'; \g" | psql
echo "drop database if exists movies \g" | psql
echo "create database movies \g" | psql
echo "create table review(URL text, review text) \g" | psql movies
echo "COPY review(URL, review) from '/var/lib/postgresql/grizzly/imdb/data.csv' delimiter '|' csv \g"| psql movies
echo "create table review_10 as select * from review limit 10 \g" | psql movies
echo "create table review_50 as select * from review limit 50 \g" | psql movies
echo "create table review_100 as select * from review limit 100 \g" | psql movies
echo "create table review_500 as select * from review limit 500 \g" | psql movies
echo "create table review_1000 as select * from review limit 1000 \g" | psql movies
