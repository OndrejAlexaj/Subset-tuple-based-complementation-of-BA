pocet_autfilt=0
pocet_ranker=0
total=0
for FILE in binary-encoding/*; do
	total=$((total+1))
	export PATH=$PATH":/home/ondrejalexaj/usr/bin"
	my=$(echo $FILE | python3 main.py)
	aut=$(autfilt "$FILE" --complement | awk -F: '$1 == "States" {print $2}' | tr -dc '0-9')
	ranker=$(../ranker/src/ranker "$FILE" --best | awk -F: '$1 == "States" {print $2}' | tr -dc '0-9')
	if [ "$my" -lt "$aut" ]; then
		echo "My algo: $my"
		echo "Autfilt: $aut"
		echo ".............."
		pocet_autfilt=$((pocet_autfilt+1))
	fi
	
	if [ "$my" -lt "$ranker" ]; then
		echo "My algo: $my"
		echo "Ranker: $ranker"
		echo ".............."
		pocet_ranker=$((pocet_ranker+1))
	fi
done

echo "------------------------------"
echo "			END					"
echo "------------------------------"
echo "Better than autfilt in $pocet_autfilt cases of total $total"
echo "Better than ranker in $pocet_ranker cases of total $total"