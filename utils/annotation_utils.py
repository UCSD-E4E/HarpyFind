#!/usr/bin/python
from lxml import etree
from osgeo import gdal

import numpy as np
import csv

import gdal_utils

def add_object(doc, xmin, ymin, xmax, ymax):
    # Create Object Tree
    obj = etree.SubElement(doc, "object")

    name = etree.SubElement(obj, "name")
    name.text = "Palm Tree"

    pose = etree.SubElement(obj, "name")
    pose.text = "Unspecified"

    truncated = etree.SubElement(obj, "truncated")
    truncated.text = "0"

    difficult = etree.SubElement(obj, "difficult")
    difficult.text = "0"

    bndbox = etree.SubElement(obj, "bndbox")

    bb_xmin = etree.SubElement(bndbox, "xmin")
    bb_xmin.text = str(xmin)

    bb_ymin = etree.SubElement(bndbox, "ymin")
    bb_ymin.text = str(ymin)

    bb_xmax = etree.SubElement(bndbox, "xmax")
    bb_xmax.text = str(xmax)

    bb_ymax = etree.SubElement(bndbox, "ymax")
    bb_ymax.text = str(ymax)

    return obj


def generate_pascal_template(imgname, username,
                               width, height):

    doc = etree.Element("annotation")

    folder = etree.SubElement(doc, "folder")
    folder.text = 'tiles'

    filename = etree.SubElement(doc, "filename")
    filename.text = imgname

    # Create Source Tree
    source = etree.SubElement(doc, "source")

    database = etree.SubElement(source, "database")
    database.text = 'HarpyFind'

    annotation = etree.SubElement(source, "annotation")
    annotation.text = 'PASCAL 2007'

    image = etree.SubElement(source, "image")
    image.text = 'flickr'

    flickrid = etree.SubElement(source, "flickrid")
    flickrid.text = 'N/A'

    # Create Owner subtree
    owner = etree.SubElement(doc, "owner")
    owner_fid = etree.SubElement(owner, "flickrid")
    owner_fid.text = 'N/A'
    name = etree.SubElement(owner, "name")
    name.text = 'N/A'

    # Create Size Tree
    size = etree.SubElement(doc, "size")
    w = etree.SubElement(size, "width")
    w.text = str(width)
    h = etree.SubElement(size, "height")
    h.text = str(height)

    # Create Segmented Tree
    segmented = etree.SubElement(doc, "segmented")
    segmented.text = "0"

    return doc

def annotate_tiles(tagfile):
    pascal_path = '../data/annotations/PASCAL/'
    tiles_path = '../data/tiles/'

    with open(tagfile, "r") as csvfile:
        tags = csv.reader(csvfile, delimiter=',')

        # skip the header
        next(tags, None)

        tileid = '0'

        for row in tags:

            if tileid != str(row[0]):

                if tileid != '0':
                    with open(pascal_path + tileid + ".xml", "w") as outfile:
                        doc = etree.tostring(doc, pretty_print=True)
                        outfile.write(doc.replace('  ', '\t'))

                tileid = str(row[0])
                print(tileid+".tif")
                tif = gdal.Open(tiles_path+tileid+".tif")
                tf = tif.GetGeoTransform()
                channel = np.array(tif.GetRasterBand(1).ReadAsArray().astype(np.float32))

                doc = generate_pascal_template(tileid, str(row[9]),
                                               channel.shape[0],
                                               channel.shape[1])

            lat1 = float(row[5])
            lon1 = float(row[6])
            lat2 = float(row[7])
            lon2 = float(row[8])
            user = str(row[9])

            xmin, ymin = gdal_utils.coord2pixel(tf, lat1, lon1)
            xmax, ymax = gdal_utils.coord2pixel(tf, lat2, lon2)
            doc.append(add_object(doc, xmin, ymin, xmax, ymax))

# doc = generate_pascal_template("test", "matt", 100, 200)
# print etree.tostring(doc, pretty_print=True).replace('  ', '\t')
annotate_tiles('../data/tags/tiles_22feb17_0657.csv')
