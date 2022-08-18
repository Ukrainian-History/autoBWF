import math
import sys
import argparse
import csv
import json
from appdirs import AppDirs
from pathlib import Path
import xml.etree.ElementTree as ET
from os import path

namespaces = {"xml": "http://www.w3.org/XML/1998/namespace",
              "ohms": "https://www.weareavp.com/nunncenter/ohms"}


def initialize_tree():
    for ns in namespaces.keys():
        ET.register_namespace(ns, namespaces[ns])


def qualified_element(ns, element):
    return "{{{0}}}{1}".format(namespaces[ns], element)


def add_child(parent, element_name, element_value='', attributes=None):
    element = ET.SubElement(parent, element_name)
    element.text = element_value
    if attributes is not None:
        for attribute in attributes.keys():
            element.set(attribute, attributes[attribute])
    return element


def write_ohms(labelfile, config):
    ohms_root = ET.Element(qualified_element("ohms", "ROOT"))
    record = add_child(ohms_root, "record")
    add_child(record, "version", "5.4")
    add_child(record, "date_nonpreferred_format", "Unknown Date")

    content_name = labelfile.replace('_labels.txt', '')
    outfile = content_name + '_ohms.xml'

    add_child(record, "title", content_name)
    add_child(record, "repository", config["originator"])
    add_child(record, "translate", "0")
    add_child(record, "media_url", "https://example.com/change-this.mp3")
    mediafile = add_child(record, "mediafile")
    add_child(mediafile, "host", "Other")
    add_child(mediafile, "clip_format", "audio")

    # parse labelfile as TSV
    with open(labelfile) as file:
        tsv_file = csv.reader(file, delimiter="\t")

        index = add_child(record, "index")
        for line in tsv_file:
            float_time = float(line[0])
            title = line[2]
            int_time = math.floor(float_time)
            if float_time-int_time > 0.8:
                int_time += 1

            point = add_child(index, "point")
            add_child(point, "time", str(int_time))
            add_child(point, "title", title)

    ET.ElementTree(ohms_root).write(outfile, xml_declaration=True, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(
        description='Convert labels exported from Audacity into index points in a minimal OHMS XML file')
    parser.add_argument('infile', nargs="+", help="WAV file(s)")
    args = parser.parse_args()

    dirs = AppDirs("autoBWF", "UHEC")
    config_file = Path(dirs.user_data_dir) / "autobwfconfig.json"

    try:
        config_text = config_file.read_text()
    except FileNotFoundError:
        print("You must first run autoBWF in order to create a default configuration file.")
        exit

    config = json.loads(config_text)

    for infile in args.infile:
        write_ohms(infile, config)


if __name__ == '__main__':
    main()
