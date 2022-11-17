pocet_autfilt=0
pocet_ranker=0
total=0

i=0

for FILE in binary-encoding/*; do
	if cat $FILE | autcross 'python3 main.py %H >%O' 'autfilt --complement %H >%O | autfilt --sba' | grep -q 'error'; then
		echo "FAIL"
	else
		echo "PASS"
	fi
	#export PATH=$PATH":/home/ondrejalexaj/usr/bin"
	echo "-----------------------------------"
	#aut=$(autfilt "$FILE" --complement | awk -F: '$1 == "States" {print $2}' | tr -dc '0-9')
	#ranker=$(../ranker/src/ranker "$FILE" --best | awk -F: '$1 == "States" {print $2}' | tr -dc '0-9')
done