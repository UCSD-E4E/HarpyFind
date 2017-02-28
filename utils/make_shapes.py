import sys
import shapefile

# Create shapefile based on csv of tags from harpy_web
# Usage: python make_shapes.py <tag_csv> <output_shp>

with open(sys.argv[1], 'r') as tag_list:
	next(tag_list)
	w = shapefile.Writer(shapefile.POLYGON)
	w.field('TILE', 'N', '9')
	for line in tag_list:
		data = line.split(',')
		bound = map(lambda x: float(x), data[5:9])
		box = [[bound[1],bound[0]],[bound[3],bound[0]],[bound[3],bound[2]],[bound[1],bound[2]]]
		w.poly(parts=[box])
		w.record(data[0])
	w.save(sys.argv[2])
