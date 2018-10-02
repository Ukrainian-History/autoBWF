import subprocess
import os

namespaces = {'dc': 'http://purl.org/dc/elements/1.1/',
              'xmp': 'http://ns.adobe.com/xap/1.0/',
              'xmpRights': "http://ns.adobe.com/xap/1.0/rights/",
              'xmpDM': "http://ns.adobe.com/xmp/1.0/DynamicMedia/",
              'autoBWF': "http://ns.ukrhec.org/autoBWF/0.1",
              'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
              'x': "adobe:ns:meta/",
              "xml": "http://www.w3.org/XML/1998/namespace"}


def get_xmp(filename):
    """New version of XMP getter using bwfmetaedit"""
    import xml.etree.ElementTree as ET

    subprocess.run(["bwfmetaedit", "--out-XMP-xml", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outfile = filename + ".XMP.xml"
    try:
        tree = ET.parse(outfile)
    except FileNotFoundError:
        md = {"interviewer": None, "interviewee": None, "owner": None,
              "metadataDate": None, "language": None, "description": None}
        return md
    root = tree.getroot()

    md = {"interviewer": root.find('.//autoBWF:Interviewer//rdf:li', namespaces),
          "interviewee": root.find('.//autoBWF:Interviewee//rdf:li', namespaces),
          "owner": root.find('.//xmpRights:Owner//rdf:li', namespaces),
          "metadataDate": root.find('.//xmp:MetadataDate', namespaces),
          "language": root.findall('.//dc:language//rdf:li', namespaces),
          "description": root.find('.//dc:description//rdf:li', namespaces)
          }

    for field in md:
        if md[field] is not None:
            if field == "language":
                md[field] = [node.text for node in md[field]]
            else:
                md[field] = md[field].text

    os.remove(outfile)
    return md


def get_bwf_tech(allow_padding, file):
    import io
    import csv

    if allow_padding:
        command = "bwfmetaedit --accept-nopadding --out-tech " + file
    else:
        command = "bwfmetaedit --out-tech " + file

    tech_csv = subprocess.check_output(command, shell=True, universal_newlines=True)
    f = io.StringIO(tech_csv)
    reader = csv.DictReader(f, delimiter=',')
    tech = next(reader)
    return tech


def get_bwf_core(allow_padding, file):
    import io
    import csv

    if allow_padding:
        command = "bwfmetaedit --accept-nopadding --out-core " + file
    else:
        command = "bwfmetaedit --out-core " + file

    core_csv = subprocess.check_output(command, shell=True, universal_newlines=True)
    f = io.StringIO(core_csv)
    reader = csv.DictReader(f, delimiter=',')
    core = next(reader)
    return core


def call_bwf(command, file, key, text):
    # deal with annoying inconsistencies in bwfmetaedit
    if key == "Timereference":
        mdkey = "TimeReference"
    elif key == "History":
        mdkey = "CodingHistory"
    else:
        mdkey = key

    # if text != self.original_md[mdkey]:
    #     subprocess.call(command + '--' + key + '="' + text + '" ' + file, shell=True)
    # TODO this checking needs to be done "upstairs" in the object, not here

    subprocess.call(command + '--' + key + '="' + text + '" ' + file, shell=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Test IO functions.')
    parser.add_argument('filename', help='WAV file to be processed')
    args = parser.parse_args()
    filename = args.filename

    print(get_xmp(filename))
