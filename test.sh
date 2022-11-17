pocet_autfilt=0
pocet_ranker=0
total=0

i=0
passed=0

for FILE in binary-encoding/*; do
	total=$((total+1))
	cat $FILE > poruchany.txt
	if cat $FILE | autcross 'python3 main.py %H 2 >%O' 'autfilt --complement %H | autfilt --sba >%O' &> ahoj.txt | cat ahoj.txt | grep -q error; then
		echo "FAIL"
		break
	else
		passed=$((passed+1))
		#echo "PASS"
	fi
	#export PATH=$PATH":/home/ondrejalexaj/usr/bin"
	#echo "-----------------------------------"
	#aut=$(autfilt "$FILE" --complement | awk -F: '$1 == "States" {print $2}' | tr -dc '0-9')
	#ranker=$(../ranker/src/ranker "$FILE" --best | awk -F: '$1 == "States" {print $2}' | tr -dc '0-9')
done