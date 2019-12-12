import argparse
import re
import csv
import sys
from os import path
from autoBWF.BWFfileIO import *


def main():
    parser = argparse.ArgumentParser(
        description='Extract metadata from BWF and create PBCore XML, possibly incorporating into existing OHMS XML')
    parser.add_argument('infile', nargs="+", help="WAV file(s)")
    args = parser.parse_args()

    output_fields = ["OriginalFilename", "FileContent", "FileUse", "INAM", "ICRD", "form", "Duration", "language",
                     "ISRC", "xmp_description", "interviewer", "interviewee", "host", "speaker",
                     "performer", "topics", "names", "events", "places", "owner", "ICOP"]

    output = csv.DictWriter(sys.stdout, output_fields)
    output.writeheader()

    for infile in args.infile:
        metadata = get_bwf_core(True, infile)
        metadata.update(get_bwf_tech(True, infile))
        metadata.update(get_xmp(infile, ["bwfmetaedit", "--specialchars", "--accept-nopadding"]))
        output.writerow({k: metadata[k] for k in output_fields if k in metadata})


if __name__ == '__main__':
    main()
