#!/bin/bash

BASEURL="https://api.deckbrew.com/mtg/cards?page="
PAGEID=1
FOLDER="jsondata/"

while true
do
	URL="${BASEURL}${PAGEID}"
	FILE="${FOLDER}${PAGEID}.json"
	echo "Fetching $PAGEID"
	curl $URL > "${FILE}"
	data=$(cat "${FILE}")

	if [ "$data" == "[]" ]; then
		echo "Reached the end !"
		exit 1
	fi

	sleep 3
	PAGEID=$((PAGEID+1))
done