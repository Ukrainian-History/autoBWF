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
    try:
        md = get_bwf_tech(filename)
    except subprocess.CalledProcessError:
        return None

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
