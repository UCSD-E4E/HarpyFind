#!/bin/bash
#
# Convert harpy_web csv into yolo label file
# Usage: process.sh <input_tif> <label_csv> <output_dir>

# integer ratio of images for training to validation
# 0 to make all images validation, -1 to make all for training
VALIDATE_RATIO=0

# image and label directories
IMAGE_DIR=$3/images
LABEL_DIR=$3/labels
echo $IMAGE_DIR $LABEL_DIR
# change separator to commas to handle csv correctly
OLDIFS=$IFS
IFS=,

iter='-1'
mkdir -p ${IMAGE_DIR}
rm -rf ${LABEL_DIR}
mkdir -p ${LABEL_DIR}

while read tileid tilelat1 tilelon1 tilelat2 tilelon2 lat1 lon1 lat2 lon2 user timestamp uuid
do
	if [ $iter -eq '-1' ]
	then
		echo "Read headers"
		iter='0'
		continue
	fi
	if [ ! -f ${IMAGE_DIR}/${tileid}.tif ]
	then
		echo "Creating ${tileid}.tif"
		# crop large tif to single tile
		gdalwarp -te $tilelon1 $tilelat2 $tilelon2 $tilelat1 $1 ${IMAGE_DIR}/${tileid}.tif

		# convert to jpg in case network can't handle tif
		convert ${IMAGE_DIR}/${tileid}.tif ${IMAGE_DIR}/${tileid}.jpg

		# put image into validation list or training list
		if [ $iter -eq $VALIDATE_RATIO ]
		then
			iter=0
			echo "$(pwd)/${IMAGE_DIR}/${tileid}.jpg" >> $3/valid.txt
		else
			iter=$(($iter + 1))
			echo "$(pwd)/${IMAGE_DIR}/${tileid}.jpg" >> $3/train.txt
		fi
	fi

	# reset separator to handle grep output
	IFS=$OLDIFS

	# get image properties
	origin=( $(gdalinfo ${IMAGE_DIR}/${tileid}.tif | grep Origin | grep -P '\-?\d+\.?\d*' -o) )
	pixel=( $(gdalinfo ${IMAGE_DIR}/${tileid}.tif | grep Pixel | grep -P '\-?\d+\.?\d*' -o) )
	size=( $(gdalinfo ${IMAGE_DIR}/${tileid}.tif | grep "Size is" | grep -P '\-?\d+\.?\d*' -o) )

	# convert latitude longitude to size relative to whole image
	bound="0"
	bound=$bound" "$(echo "((((${lon1}) + (${lon2})) / 2 ) - (${origin[0]})) / (${pixel[0]}) / (${size[0]})" | bc -l)
	bound=$bound" "$(echo "((((${lat1}) + (${lat2})) / 2 ) - (${origin[1]})) / (${pixel[1]}) / (${size[1]})" | bc -l)
	bound=$bound" "$(echo "((${lon2}) - (${lon1})) / (${pixel[0]}) / (${size[0]})" | bc -l)
	bound=$bound" "$(echo "((${lat2}) - (${lat1})) / (${pixel[1]}) / (${size[1]})" | bc -l)
	echo "$bound" >> ${LABEL_DIR}/${tileid}.txt
	echo $tileid
	IFS=,
done < $2
IFS=$OLDIFS
