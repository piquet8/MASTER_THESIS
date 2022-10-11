echo '{ "positive_traces": [' >> sample2.json;

for i in *_s.json;
do cat "$i" >> sample2.json && echo ', ' >> sample2.json;
done;

echo '], "negative_traces": [' >> sample2.json;

for i in *_f.json;
do cat "$i" >> sample2.json && echo ', ' >> sample2.json;
done;

echo '] }' >> sample2.json;