import subprocess
import os
import xml.etree.ElementTree as ET

namespaces = {'dc': 'http://purl.org/dc/elements/1.1/',
              'xmp': 'http://ns.adobe.com/xap/1.0/',
              'xmpRights': "http://ns.adobe.com/xap/1.0/rights/",
              'xmpDM': "http://ns.adobe.com/xmp/1.0/DynamicMedia/",
              'autoBWF': "http://ns.ukrhec.org/autoBWF/0.1",
              'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
              'x': "adobe:ns:meta/",
              "xml": "http://www.w3.org/XML/1998/namespace"}


def get_xmp(filename, base_command):
    command = base_command
    command.extend(["--out-XMP-xml", filename])
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outfile = filename + ".XMP.xml"
    try:
        tree = ET.parse(outfile)
    except FileNotFoundError:
        md = {"interviewer": "", "interviewee": "", "owner": "",
              "metadataDate": "", "language": "", "description": ""}
        return md
    root = tree.getroot()

    def check_li_child(element, xpath):
        # provide backwards compatibility for XMP
        # saved using exempi and python-metadata-toolkit
        node = element.find(xpath + "//rdf:li", namespaces)
        if node is not None:
            return node
        else:
            return element.find(xpath, namespaces)

    md = {"interviewer": check_li_child(root, './/autoBWF:Interviewer'),
          "interviewee": check_li_child(root, './/autoBWF:Interviewee'),
          "owner": check_li_child(root, './/xmpRights:Owner'),
          "metadataDate": root.find('.//xmp:MetadataDate', namespaces),
          "language": root.findall('.//dc:language//rdf:li', namespaces),
          "description": check_li_child(root, './/dc:description')
          }

    for field in md:
        if md[field] is not None:
            if field == "language":
                md[field] = ";".join([node.text for node in md[field]])
            else:
                md[field] = md[field].text
        else:
            md[field] = ""

    os.remove(outfile)
    return md


def set_xmp(md, filename, base_command):
    from datetime import datetime

    def qualified_element(ns, element):
        return "{{{0}}}{1}".format(namespaces[ns], element)

    for ns in namespaces.keys():
        ET.register_namespace(ns, namespaces[ns])

    root = ET.Element(qualified_element("x", "xmpmeta"))
    rdf = ET.SubElement(root, qualified_element("rdf", "RDF"))
    rdf_description = ET.SubElement(rdf, qualified_element("rdf", "Description"))

    # if set_xmp() is being called, then some metadata somewhere has changed,
    # and therefore we MUST have an xmp:MetadataDate
    date = ET.SubElement(rdf_description, qualified_element("xmp", "MetadataDate"))
    date.text = datetime.now().isoformat()

    if md["description"] != "":
        description = ET.SubElement(rdf_description, qualified_element("dc", "description"))
        alt = ET.SubElement(description, qualified_element("rdf", "Alt"))
        li = ET.SubElement(alt, qualified_element("rdf", "li"))
        li.set("xml:lang", "x-default")
        li.text = md["description"]
    if md["owner"] != "":
        owner = ET.SubElement(rdf_description, qualified_element("xmpRights", "Owner"))
        owner_bag = ET.SubElement(owner, qualified_element("rdf", "Bag"))
        owner_item = ET.SubElement(owner_bag, qualified_element("rdf", "li"))
        owner_item.text = md["owner"]
    if md["interviewer"] != "":
        interviewer = ET.SubElement(rdf_description, qualified_element("autoBWF", "Interviewer"))
        interviewer.text = md["interviewer"]
    if md["interviewee"] != "":
        interviewee = ET.SubElement(rdf_description, qualified_element("autoBWF", "Interviewee"))
        interviewee.text = md["interviewee"]
    if md["language"] != "":
        language = ET.SubElement(rdf_description, qualified_element("dc", "language"))
        language_bag = ET.SubElement(language, qualified_element("rdf", "Bag"))
        for lang in md["language"].split(';'):
            language_item = ET.SubElement(language_bag, qualified_element("rdf", "li"))
            language_item.text = lang

    xmlfile = filename + ".XMP.xml"
    ET.ElementTree(root).write(xmlfile)
    command = base_command
    command.extend(['--in-XMP=' + xmlfile, filename])
    subprocess.run(command)
    os.remove(xmlfile)


def get_bwf_tech(allow_padding, file):
    import io
    import csv

    if allow_padding:
        command = ["bwfmetaedit", "--accept-nopadding", "--out-tech", file]
    else:
        command = ["bwfmetaedit", "--out-tech", file]

    tech_csv = subprocess.check_output(command, universal_newlines=True)
    f = io.StringIO(tech_csv)
    reader = csv.DictReader(f, delimiter=',')
    tech = next(reader)
    return tech


def get_bwf_core(allow_padding, file):
    import io
    import csv

    if allow_padding:
        command = ["bwfmetaedit", "--accept-nopadding", "--out-core", file]
    else:
        command = ["bwfmetaedit", "--out-core", file]

    core_csv = subprocess.check_output(command, universal_newlines=True)
    f = io.StringIO(core_csv)
    reader = csv.DictReader(f, delimiter=',')
    core = next(reader)
    return core


def call_bwf(base_command, file, mdkey, text):
    # deal with annoying inconsistencies in bwfmetaedit
    if mdkey == "TimeReference":
        key = "Timereference"
    elif mdkey == "CodingHistory":
        key = "History"
    else:
        key = mdkey

    command = base_command
    command.extend(['--' + key + "=" + text, file])
    subprocess.run(command)


if __name__ == "__main__":
    pass
