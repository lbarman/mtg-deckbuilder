#!/bin/bash

FOLDER="thumbnails"
FILE="imagestoget.txt"

grep -hs "image_url" -R jsondata | sed -e "s/        \"image_url\": \"//" | sed -e "s/\",//" > "${FOLDER}/${FILE}"

cd "$FOLDER"
wget -N -i "${FILE}" --wait=1 --random-wait


rm -f $FILE