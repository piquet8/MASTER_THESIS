
# use nullglob in case there are no matching files
shopt -s nullglob dotglob

# create an array with all the filer/dir inside ~/myDir
arr_s=(*_s.json)
echo "${#arr_s[@]}"
echo "${arr_s[@]}"

arr_f=(*_f.json)
echo "${#arr_f[@]}"
echo "${arr_f[@]}"

t=$((${#arr_s[@]} $i - 1 ))
k=$((${#arr_f[@]} $i - 1 ))

echo $t
echo $k
echo ${arr_f[@]}

echo '{ "positive_traces": [' >> sample.json;

for ((i=0; i<$t; i++)); do
    cat "${arr_s[$i]}" >> sample.json && echo ', ' >> sample.json;
done

cat "${arr_s[$t]}" >> sample.json;

echo '], "negative_traces": [' >> sample.json;

for ((i=0; i<$k; i++)); do
    cat "${arr_f[$i]}" >> sample.json && echo ', ' >> sample.json;
done

cat "${arr_s[$k]}" >> sample.json;

echo '] }' >> sample.json;
