#!/bin/bash

TIMEFORMAT="%R seconds"
sizes=( 10 50 100 500 1000 )
runs=1

echo "========GRIZZLY=========="

for s in "${sizes[@]}"
do
	echo -e "Size: $s \n"
	for (( c=1; c<=$runs; c++ ))
	do
		cat eval_roberta_grizzly.py | sed "s/SIZE/$s/g"	> temp
		time python3 temp
	      	echo -e "\n"	
	done
done

echo "========PANDAS=========="

for s in "${sizes[@]}"
do
        echo -e "Size: $s \n"
        for (( c=1; c<=$runs; c++ ))
	do
                cat eval_roberta_pandas.py | sed "s/SIZE/$s/g" > temp
                time python3 temp 
        	echo -e "\n"
	done
done

echo "========MODIN=========="

for s in "${sizes[@]}"
do
        echo -e "Size: $s \n"
        for (( c=1; c<=$runs; c++ ))
	do
                cat eval_roberta_modin.py | sed "s/SIZE/$s/g" > temp
                time python3 temp
		echo -e "\n"
        done
done


