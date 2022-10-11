#!/bin/bash

shopt -s nullglob
logfiles_s=(*_s.json)
x_s=${#logfiles_s[@]}

shopt -s nullglob
logfiles_f=(*_f.json)
x_f=${#logfiles_f[@]}

x_s=$(( $x_s - 1 ))
echo $x_s

x_f=$(( $x_f - 1 ))
echo $x_f

echo '{ "positive_traces": [' >> sample.json;

t=0 
for i in *_s.json;
do if [ $t -lt $x_s ]; 
 then 
	cat "$i" >> sample.json && echo ', ' >> sample.json;
	t=$(( $t + 1 ))
 else
 	cat "$i" >> sample.json 
 	t=$(( $t + 1 ))
fi
done

echo '], "negative_traces": [' >> sample.json;

k=0 
for i in *_f.json;
do if [ $k -lt $x_f ]; 
 then 
	cat "$i" >> sample.json && echo ', ' >> sample.json;
	k=$(( $k + 1 ))
 else
 	echo $k
 	cat "$i" >> sample.json 
 	k=$(( $k + 1 ))
fi
done

echo '] }' >> sample.json;

