#!/bin/bash
#
# Convert the output of yolo to the format of the csv from harpy_web
# Usage: post.sh <input_data> <image_dir> <output_csv>

# required confidence to add a bounding box to the csv
THRESHOLD=0.1

# directory holding all tif files
# output header
echo 'tileid,tilelat1,tilelon1,tilelat2,tilelon2,lat1,lon1,lat2,lon2,user,timestamp,uuid' > $3
while read name prob minx miny maxx maxy
do
	# make sure only boxes above a certain confidence are added
	if [ $(echo "$prob > $THRESHOLD" | bc -l) -eq 1 ]
	then
		# get the location parameters of the image
		origin=( $(gdalinfo $2/${name}.tif | grep Origin | grep -P '\-?\d+\.?\d*' -o) )
		pixel=( $(gdalinfo $2/${name}.tif | grep Pixel | grep -P '\-?\d+\.?\d*' -o) )
		size=( $(gdalinfo $2/${name}.tif | grep "Size is" | grep -P '\-?\d+\.?\d*' -o) )

		# convert the pixel coordinates to latitudes and longitudes
		line=$name
		line=$line","$(echo "${origin[1]}" | bc -l)
		line=$line","$(echo "${origin[0]}" | bc -l)
		line=$line","$(echo "${origin[1]} + (${pixel[1]}) * ${size[1]}" | bc -l)
		line=$line","$(echo "${origin[0]} + (${pixel[0]}) * ${size[0]}" | bc -l)
		line=$line","$(echo "${origin[1]} + (${pixel[1]}) * ${maxy}" | bc -l)
		line=$line","$(echo "${origin[0]} + (${pixel[0]}) * ${minx}" | bc -l)
		line=$line","$(echo "${origin[1]} + (${pixel[1]}) * ${miny}" | bc -l)
		line=$line","$(echo "${origin[0]} + (${pixel[0]}) * ${maxx}" | bc -l)

		# put placeholder values for the user, timestamp, and tag uuid
		line=$line",0,0,0"
		echo "$line" >> $3
	fi
done < $1
