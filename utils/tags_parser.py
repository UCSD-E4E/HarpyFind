import os
import sys
import csv
import gdal_utils


def tag_parser(filename, log="../data/tiles/log"):
    report = []

    with open(filename, "r") as csvfile:
        tags = csv.reader(csvfile, delimiter=',')

        # skip the header
        next(tags, None)

        for row in tags:

            # Make sure the directory for user exists
            if not os.path.exists("../data/tiles/"+row[4]):
                os.makedirs("../data/tiles/"+row[4])

            files = os.listdir("../data/tiles/"+row[4])

            if row[6]+'.tif' not in files:

                lat1 = float(row[0])
                lon1 = float(row[1])
                lat2 = float(row[2])
                lon2 = float(row[3])

                outfile = '../data/tiles/'+row[4]+'/'+row[6]+'.tif'

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
    else:
        tag_parser("../data/tags/tags_jan29_1137.csv")
