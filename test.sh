pocet_autfilt=0
pocet_ranker=0
total=0

i=0

for FILE in binary-encoding/*; do
	if [$i -eq 1000]; then
		break
	fi
	total=$((total+1))
	export PATH=$PATH":/home/ondrejalexaj/usr/bin"
	my=$(python3 main.py $FILE 0 1)
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