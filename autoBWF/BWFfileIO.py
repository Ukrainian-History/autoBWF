"""Perform IO on BWF files.

Convenience functions for reading from and writing to BWF files using bwfmetaedit subprocess calls.

Attributes:
    bwfmetaedit (list): List of strings to be passed to subprocess.run(). This list should be appended to (after
        copy()-ing) in order to perform the needed function. Its primary role is to keep track of whether
        the "--accept-nopadding" option is or is not to be used. It may be modified by other modules
        (such as autoBWF.py) that import this module.

    namespaces (dict): Dict of XMP namespace URIs
"""

import subprocess
import os
import xml.etree.ElementTree as ET

bwfmetaedit = ["bwfmetaedit", "--specialchars"]

namespaces = {'dc': 'http://purl.org/dc/elements/1.1/',
              'xmp': 'http://ns.adobe.com/xap/1.0/',
              'xmpRights': "http://ns.adobe.com/xap/1.0/rights/",
              'xmpDM': "http://ns.adobe.com/xmp/1.0/DynamicMedia/",
              'autoBWF': "http://ns.ukrhec.org/autoBWF/0.1",
              'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
              'x': "adobe:ns:meta/",
              "xml": "http://www.w3.org/XML/1998/namespace"}


def get_xmp(filename):
    """Runs bwfmetaedit to extract XMP metadata from a BWF file.

    Args:
        filename (str): The name of the target BWF file.

    Returns:
        dict:  Dict of metadata values indexed by the field name. If field is empty, the value is an empty string.
    """

    command = bwfmetaedit.copy()
    command.extend(["--out-XMP-xml", filename])
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outfile = filename + ".XMP.xml"
    try:
        tree = ET.parse(outfile)
    except FileNotFoundError:
        md = {"interviewer": "", "interviewee": "", "owner": "",
              "metadataDate": "", "language": "", "xmp_description": "",
              "form": "", "host": "", "speaker": "", "performer": "",
              "topics": "", "names": "", "events": "", "places": "", "creator": ""
              }
        return md
    root = tree.getroot()

    def check_li_child(element, xpath):
        """Provides backwards compatibility for XMP saved using exempi and python-metadata-toolkit"""
        node = element.find(xpath + "//rdf:li", namespaces)
        if node is not None:
            return node
        else:
            return element.find(xpath, namespaces)

    md = {
        "owner": check_li_child(root, './/xmpRights:Owner'),
        "metadataDate": root.find('.//xmp:MetadataDate', namespaces),
        "language": root.findall('.//dc:language//rdf:li', namespaces),
        "xmp_description": check_li_child(root, './/dc:description'),
        "interviewer": check_li_child(root, './/autoBWF:Interviewer'),
        "interviewee": check_li_child(root, './/autoBWF:Interviewee'),
        "form": check_li_child(root, './/autoBWF:Form'),
        "host": check_li_child(root, './/autoBWF:Host'),
        "speaker": check_li_child(root, './/autoBWF:Speaker'),
        "performer": check_li_child(root, './/autoBWF:Performer'),
        "topics": check_li_child(root, './/autoBWF:Topics'),
        "names": check_li_child(root, './/autoBWF:Names'),
        "events": check_li_child(root, './/autoBWF:Events'),
        "places": check_li_child(root, './/autoBWF:Places'),
        "creator": check_li_child(root, './/dc:creator'),
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


def set_xmp(md, filename):
    """Runs bwfmetaedit to extract XMP metadata from a BWF file.

    Args:
        md (dict): Dict of metadata values indexed by the field name.
            If field is empty, the value should be an empty string.
        filename (str): The name of the target BWF file.
    """

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

    if md["xmp_description"] != "":
        description = ET.SubElement(rdf_description, qualified_element("dc", "description"))
        alt = ET.SubElement(description, qualified_element("rdf", "Alt"))
        li = ET.SubElement(alt, qualified_element("rdf", "li"))
        li.set("xml:lang", "x-default")
        li.text = md["xmp_description"]
    if md["owner"] != "":
        owner = ET.SubElement(rdf_description, qualified_element("xmpRights", "Owner"))
        owner_bag = ET.SubElement(owner, qualified_element("rdf", "Bag"))
        owner_item = ET.SubElement(owner_bag, qualified_element("rdf", "li"))
        owner_item.text = md["owner"]
    if md["creator"] != "":
        creator = ET.SubElement(rdf_description, qualified_element("dc", "creator"))
        creator_seq = ET.SubElement(creator, qualified_element("rdf", "Seq"))
        creator_item = ET.SubElement(creator_seq, qualified_element("rdf", "li"))
        creator_item.text = md["creator"]

    if md["interviewer"] != "":
        interviewer = ET.SubElement(rdf_description, qualified_element("autoBWF", "Interviewer"))
        interviewer.text = md["interviewer"]
    if md["interviewee"] != "":
        interviewee = ET.SubElement(rdf_description, qualified_element("autoBWF", "Interviewee"))
        interviewee.text = md["interviewee"]
    if md["form"] != "":
        interviewee = ET.SubElement(rdf_description, qualified_element("autoBWF", "Form"))
        interviewee.text = md["form"]
    if md["host"] != "":
        interviewee = ET.SubElement(rdf_description, qualified_element("autoBWF", "Host"))
        interviewee.text = md["host"]
    if md["speaker"] != "":
        interviewee = ET.SubElement(rdf_description, qualified_element("autoBWF", "Speaker"))
        interviewee.text = md["speaker"]
    if md["performer"] != "":
        interviewee = ET.SubElement(rdf_description, qualified_element("autoBWF", "Performer"))
        interviewee.text = md["performer"]
    if md["topics"] != "":
        interviewee = ET.SubElement(rdf_description, qualified_element("autoBWF", "Topics"))
        interviewee.text = md["topics"]
    if md["names"] != "":
        interviewee = ET.SubElement(rdf_description, qualified_element("autoBWF", "Names"))
        interviewee.text = md["names"]
    if md["events"] != "":
        interviewee = ET.SubElement(rdf_description, qualified_element("autoBWF", "Events"))
        interviewee.text = md["events"]
    if md["places"] != "":
        interviewee = ET.SubElement(rdf_description, qualified_element("autoBWF", "Places"))
        interviewee.text = md["places"]

    if md["language"] != "":
        language = ET.SubElement(rdf_description, qualified_element("dc", "language"))
        language_bag = ET.SubElement(language, qualified_element("rdf", "Bag"))
        for lang in md["language"].split(';'):
            language_item = ET.SubElement(language_bag, qualified_element("rdf", "li"))
            language_item.text = lang

    xmlfile = filename + ".XMP.xml"
    ET.ElementTree(root).write(xmlfile)
    command = bwfmetaedit.copy()
    command.extend(['--in-XMP=' + xmlfile, filename])
    subprocess.run(command)
    os.remove(xmlfile)


def check_wave(filename):
    """Confirm that filename is a legitimate Wave file.

    This is done by running bwfmetaedit to extract the technical metadata, which should work even if there is no
    pre-existing BWF chunk.

    Args:
        filename (str): The name of the file.

    Returns:
        dict: Technical metadata values indexed by the field name. If field is empty, the value is an empty string.
            If filename is not a Wave file, then the return value is None.
    """
    md = get_bwf_tech(filename)
    if md["Errors"] == "":
        return md
    else:
        return None


def get_bwf_tech(file, verify_digest=False):
    """Runs bwfmetaedit to extract BWF technical metadata from a BWF file.

    Args:
        file (str): The name of the target BWF file.
        verify_digest (bool): If True, add "--MD5-verify" to the bwfmetaedit call.

    Returns:
        dict: Metadata values indexed by the field name. If field is empty, the value is an empty string.
    """

    import io
    import csv

    command = bwfmetaedit.copy()
    command.append("--out-tech")
    if verify_digest:
        command.extend(["--MD5-verify", file])
    else:
        command.append(file)

    tech_csv = subprocess.check_output(command, universal_newlines=True)
    f = io.StringIO(tech_csv)
    reader = csv.DictReader(f, delimiter=',')
    tech = next(reader)
    return tech


def parse_bwf_description(description):
    """Parses a BWF Description string based on a hard-coded pre-defined convention.

    Args:
        description (str): The BWF Description string.

    Returns:
        dict: Metadata values indexed by the field name. If field is empty, the value is an empty string.
    """

    import re

    md = {}

    m = re.compile(r'File content: (.+); File use: (.+); Original filename: (.+)').match(description)
    if m:
        matches = m.groups()
        md["FileContent"] = matches[0]
        md["FileUse"] = matches[1]
        md["OriginalFilename"] = matches[2]
    else:
        md["FileContent"] = ""
        md["FileUse"] = ""
        md["OriginalFilename"] = ""

    return md


def get_bwf_core(file):
    """Runs bwfmetaedit to extract BWF core metadata from a BWF file.

    Args:
        file (str): The name of the target BWF file.

    Returns:
        dict: Metadata values indexed by the field name. If field is empty, the value is an empty string.
    """

    import io
    import csv

    command = bwfmetaedit.copy()
    command.extend(["--out-core", file])

    core_csv = subprocess.check_output(command, universal_newlines=True)
    f = io.StringIO(core_csv)
    reader = csv.DictReader(f, delimiter=',')
    core = next(reader)
    for key in core.keys():
        if core[key] is None:
            core[key] = ""

    core.update(parse_bwf_description(core["Description"]))
    return core


if __name__ == "__main__":
    pass
