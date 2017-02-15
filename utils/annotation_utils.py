#!/usr/bin/python
import lxml.etree
import lxml.builder

def generate_pascal_annotation():

    E = lxml.builder.ElementMaker()
    ANNOTATION = E.annotation
    FOLDER = E.folder
    FIELD1 = E.field1
    FIELD2 = E.field2

    the_doc = ANNOTATION(
                FOLDER('TEST')
            )

    doc = lxml.etree.tostring(the_doc, pretty_print=True)

    with open("../data/annotations/test.xml", "w") as outfile:
        outfile.write(doc)

generate_pascal_annotation()
