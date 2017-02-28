import cv2
import numpy
import sys
import os

# Draw boxes on images based on yolo data
# Usage: python draw_box.py <box_list> <image_dir> <output_dir>

# transparency of drawn boxes
ALPHA = 0.3

if not os.path.exists(sys.argv[3]):
	os.makedirs(sys.argv[3])
last_name = ''
cur_image = None
overlay = None
with open(sys.argv[1], 'r') as tag_list
	for line in tag_list:
		data = line.split(' ')
		if float(data[1]) > 0.1:
			if (data[0] != last_name):
				if cur_image is not None:
					cur_image = cv2.addWeighted(overlay, ALPHA, cur_image, 1 - ALPHA, 0)
					cv2.imwrite(sys.argv[3] + '/' + last_name + '.jpg', cur_image)
				last_name = data[0]
				cur_image = cv2.imread(sys.argv[2] + '/' + last_name + '.jpg')
				overlay = cv2.imread(sys.argv[2] + '/' + last_name + '.jpg')
			cv2.rectangle(overlay, (int(float(data[2])),
				int(float(data[3]))),
				(int(float(data[4])),
				int(float(data[5]))), (255,0,255), thickness=20)
