#!/bin/bash

TIMEFORMAT="%R seconds"
sizes=( 100000 500000 1000000 1500000 2000000 2500000 3000000 )
runs=1
echo "========GRIZZLY=========="

for s in "${sizes[@]}"
do
	echo "===================================="
	echo -e "Size: $s\n"
        for (( c=1; c<=$runs; c++ ))
	do
		cat eval_external_grizzly.py | sed "s/SIZE/$s/g" > temp.py
		time python3 temp.py  
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
                cat eval_external_pandas.py | sed "s/SIZE/$s/g" > temp.py
		time python3 temp.py
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
                cat eval_external_modin.py | sed "s/SIZE/$s/g" > temp.py
                time python3 temp.py
		echo -e "\n"
        done
done
