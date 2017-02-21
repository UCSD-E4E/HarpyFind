#!/usr/bin/python
import lxml.etree
import lxml.builder

import csv

def generate_pascal_annotation():

    E = lxml.builder.ElementMaker()
    ANNOTATION = E.annotation
    FOLDER = E.folder
    FILENAME = E.filename
    SOURCE = E.source
    DATABASE = E.database
    IMAGE = E.image
    FLICKRID = E.flickrid
    OWNER = E.owner
    NAME = E.name
    SIZE = E.size
    WIDTH = E.width
    HEIGHT = E.height
    DEPTH = E.depth
    SEGMENTED = E.segmented
    OBJECT = E.object
    POSE = E.pose
    TRUNCATED = E.truncated
    DIFFICULT = E.difficult
    BNDBOX = E.bndbox
    XMIN = E.xmin
    YMIN = E.ymin
    XMAX = E.xmax
    YMAX = E.ymax
    LAT1 = E.lat1
    LON1 = E.lon1
    LAT2 = E.lat2
    LON2 = E.lon2
    USER = E.user
    i = 0

    with open("../data/annotations/test.csv","rb") as test_in:
        reader = csv.DictReader(test_in)
        for row in reader:
            i = i + 1
            new_xml_doc = ANNOTATION(
                            FOLDER('INSERT FOLDER NAME'),
                            FILENAME('INSERT FILENAME'),
                            SOURCE(
                                DATABASE('IS THIS NEEDED?'),
                                ANNOTATION('IS THIS NEEDED?'),
                                IMAGE('IS THIS NEEDED?'),
                                FLICKRID('IS THIS NEEDED?')
                            ),
                            OWNER(
                                FLICKRID('IS THIS NEEDED?'),
                                NAME('IS THIS NEEDED?')
                            ),
                            SIZE(
                                WIDTH('INSERT WIDTH'),
                                HEIGHT('INSERT HEIGHT'),
                                DEPTH('INSERT DEPTH') # RGB
                            ),
                            SEGMENTED('IS THIS NEEDED?'),
                            OBJECT(
                                NAME('INSERT NAME'),
                                POSE('IS THIS NEEDED?'),
                                TRUNCATED('IS THIS NEEDED?'),
                                DIFFICULT('IS THIS NEEDED?'),
                                BNDBOX(
                                    XMIN('INSERT XMIN'),
                                    YMIN('INSERT YMIN'),
                                    XMAX('INSERT XMAX'),
                                    YMAX('INSERT YMAX')
                                ),
                                LAT1(row['lat1']),
                                LON1(row['lon1']),
                                LAT2(row['lat2']),
                                LON2(row['lon2']),
                                USER(row['user'])
                            )
                        )
            doc = lxml.etree.tostring(new_xml_doc, pretty_print=True)
            with open("../data/annotations/test" + str(i) + ".xml", "w") as outfile:
                outfile.write(doc)

generate_pascal_annotation()
