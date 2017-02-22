import os
import sys
import csv
import gdal_utils

def tile_parser(filename, log="../data/tiles/log"):
    tile_path = '../data/tiles'

    with open(filename, "r") as csvfile:
        tags = csv.reader(csvfile, delimiter=',')

        # skip the header
        next(tags, None)

        # Make sure the directory for tiles
        if not os.path.exists(tile_path):
            os.makedirs(tile_path)

        files = [file.strip('.tif') for file in os.listdir(tile_path)]

        for row in tags:

            if row[0] not in files:

                tileID = int(row[0])

                # HACK: Need to get bryan to change ordering
                lat1 = float(row[4])
                lon1 = float(row[1])
                lat2 = float(row[2])
                lon2 = float(row[3])

                # lat1 = float(row[1])
                # lon1 = float(row[2])
                # lat2 = float(row[3])
                # lon2 = float(row[4])

                files.append(str(row[0]))

                outfile = tile_path+'/'+row[0]+'.tif'

                res = gdal_utils.trim(lat1, lon1, lat2, lon2,
                                      '../data/bfree_ortho.tif', outfile)
                print(row[0])
                # print(res)


def tag_parser(filename, log="../data/tiles/log"):
    report = []

    with open(filename, "r") as csvfile:
        tags = csv.reader(csvfile, delimiter=',')

        # skip the header
        next(tags, None)

        for row in tags:

            # Make sure the directory for user exists
            if not os.path.exists("../data/trees/"+row[4]):
                os.makedirs("../data/trees/"+row[4])

            files = os.listdir("../data/trees/"+row[4])

            if row[6]+'.tif' not in files:

                lat1 = float(row[0])
                lon1 = float(row[1])
                lat2 = float(row[2])
                lon2 = float(row[3])

                outfile = '../data/trees/'+row[4]+'/'+row[6]+'.tif'

                res = gdal_utils.trim(lat1, lon1, lat2, lon2,
                                      '../data/bfree_ortho.tif', outfile)

                report.append([res, row[4], row[6]])

    failed = 0

    with open(log, "w") as logfile:
        for result in report:
            if result[0][0] == 1:
                failed = failed + 1
                logfile.write("Failed to trim: "+result[1]+"/"+result[2]+"\n")
                logfile.write(result[0][1])

    if failed > 0:
        print("Failed to parse "+str(failed)+".\n Please see log file "+log)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tag_parser(sys.argv[1])
        tile_parser(sys.argv[1])
    else:
        # tag_parser("../data/tags/tags_jan29_1137.csv")
        tile_parser("../data/tags/tiles_22feb17_0657.csv")
