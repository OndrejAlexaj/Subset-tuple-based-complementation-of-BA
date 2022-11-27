#!/bin/bash
pocet_autfilt=0
pocet_ranker=0
total=0

i=0
passed=0

for FILE in binary-encoding/*; do
	total=$((total+1))
	passed=$((passed+1))
	#cat $FILE > poruchany.txt
	cat $FILE | autcross 'python3 main.py %H 4 >%O' 'autfilt --complement %H | autfilt --sba >%O' &> ahoj.txt
	obsah=$(<ahoj.txt)
	if [[ $obsah == *"error"* ]]; then
		#echo "FAILED"
		#echo $FILE
		passed=$((passed-1))
	fi
	#export PATH=$PATH":/home/ondrejalexaj/usr/bin"
	#echo "-----------------------------------"
	#aut=$(autfilt "$FILE" --complement | awk -F: '$1 == "States" {print $2}' | tr -dc '0-9')
	#ranker=$(../ranker/src/ranker "$FILE" --best | awk -F: '$1 == "States" {print $2}' | tr -dc '0-9')
done

echo "Passed: $passed / $total"