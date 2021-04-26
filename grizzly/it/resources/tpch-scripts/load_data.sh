pushd /home/actian/tpch-dbgen
for i in `ls *.tbl`; do
  table=${i/.tbl/}
  echo "Loading $table..."
  sed 's/|$//' $i > /tmp/$i
  psql -U grizzly -h cloud01 -d tpch_partitioned -q -c "TRUNCATE $table"
  psql -U grizzly -h cloud01 -d tpch_partitioned -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
done
popd
