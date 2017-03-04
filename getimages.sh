#!/bin/bash

FOLDER="thumbnails"
FILE="imagestoget.txt"

grep -hs "image_url" -R jsondata | sed -e "s/        \"image_url\": \"//" | sed -e "s/\",//" > "${FOLDER}/${FILE}"

cd "$FOLDER"
wget -nc -i "${FILE}"


rm -f $FILE
