import gdal
import sys
import math

# Split GeoTIFF into smaller tiles
# Usage: python generate_tiles.py <input_tif> <output_csv>

# size of tiles in meters
TILE_SIZE = 100

ORIGIN_SHIFT = 2 * math.pi * 6378137 / 2.0

def LatLonToMeters(lat, lon):
	mx = lon * ORIGIN_SHIFT / 180.0
	my = math.log(math.tan((90 + lat) * math.pi / 360.0)) / (math.pi / 180.0)

	my = my * ORIGIN_SHIFT / 180.0
	return mx, my

def MetersToLatLon(mx, my):
	lon = (mx / ORIGIN_SHIFT) * 180.0
	lat = (my / ORIGIN_SHIFT) * 180.0

	lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
	return lat, lon

img = gdal.Open(sys.argv[1])
gt = img.GetGeoTransform()
width = img.RasterXSize;
height = img.RasterYSize;

minLon = gt[0]
minLat = gt[3] + width * gt[4] + height * gt[5]
maxLon = gt[0] + width * gt[1] + height * gt[2]
maxLat = gt[3]

minx, miny = LatLonToMeters(minLat, minLon)
maxx, maxy = LatLonToMeters(maxLat, maxLon)

with open(sys.argv[2], 'w') as out:
	out.write('tileid,tilelat1,tilelon1,tilelat2,tilelon2,lat1,lon1,lat2,lon2,user,timestamp,uuid\n')

	xPos = minx
	i = 1
	while xPos < maxx:
		yPos = miny
		while yPos < maxy:
			lat2, lon1 = MetersToLatLon(xPos, yPos)
			lat1, lon2 = MetersToLatLon(xPos + TILE_SIZE, yPos + TILE_SIZE)
			out.write(str(i)+','+str(lat1)+','+str(lon1)+','+str(lat2)+','+str(lon2)+',0,0,0,0,0,0,0\n')
			yPos += TILE_SIZE
			i += 1
		xPos += TILE_SIZE
