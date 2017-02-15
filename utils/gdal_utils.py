from osgeo import gdal
import subprocess


def pixel2coord(gt, x, y):
    """Returns global coordinates from pixel x, y coordinates"""
    lat = gt[0] + x*gt[1] + y*gt[2]
    lon = gt[3] + x*gt[4] + y*gt[5]

    return lat, lon


def coord2pixel(gt, lat, lon):
    """Transforms lat/lon coordinates to pixel coordinates"""
    x = int(round((lon-gt[0])/gt[1]))
    y = int(round((lat-gt[3])/gt[5]))

    return x, y


def trim(lat1, lon1, lat2, lon2, infile, outfile):
    '''
    Calls gdal_translate using the provided arguments to trim a larger tif
    file into a smaller one based on the upper left and lower right lat/lon
    pairs.

        Args:
            lat1, lon1 (float): Upper left corner lat/lon

            lat2, lon2 (float): Lower right corner lat/lon

        Return:
            returncode (int): Return code from calling gdal_translate

    '''
    transform = gdal.Open(infile).GetGeoTransform()

    x1, y1 = coord2pixel(transform, lat1, lon1)
    x2, y2 = coord2pixel(transform, lat2, lon2)

    args = ['gdal_translate', '-srcwin']
    args.extend([str(x1), str(y1), str(x2-x1), str(y2-y1), infile, outfile])

    try:
        res = subprocess.check_output(args, stderr=subprocess.STDOUT)
    except Exception as ex:
        res = ex.returncode, str(ex.output)

    return res


if __name__ == "__main__":
    infile = "../data/bfree_ortho.tif"
    transform = gdal.Open(infile).GetGeoTransform()
