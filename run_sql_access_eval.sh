#!/bin/bash

TIMEFORMAT="%R seconds"
sizes=( 8500000 17000000 25500000 34000000 42500000 )
runs=1
echo "========GRIZZLY=========="

for s in "${sizes[@]}"
do
	echo "===================================="
	echo -e "Size: $s\n"
	for (( c=1; c<=$runs; c++ ))	
	do
		cat eval_sql_access_grizzly.py | sed "s/SIZE/$s/g" > temp.py
		time python temp.py
		echo -e "\n"
	done
done

echo "========PANDAS=========="

for s in "${sizes[@]}"
do
	echo "===================================="
        echo -e "Size: $s\n"
        for (( c=1; c<=$runs; c++ ))
        do
                cat eval_sql_access_pandas.py | sed "s/SIZE/$s/g" > temp.py
		time python temp.py
		echo -e "\n"
        done
done

echo "========MODIN=========="

for s in "${sizes[@]}"
do
        echo "===================================="
        echo -e "Size: $s\n"
        for (( c=1; c<=$runs; c++ ))
        do
                cat eval_sql_access_modin.py | sed "s/SIZE/$s/g" > temp.py
       		time python temp.py
		echo -e "\n"
	done
done
