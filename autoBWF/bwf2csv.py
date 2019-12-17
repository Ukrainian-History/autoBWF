import argparse
import re
import csv
import sys
from os import path
from autoBWF.BWFfileIO import *


def main():
    parser = argparse.ArgumentParser(
        description='Extract metadata from BWF and create PBCore XML, possibly incorporating into existing OHMS XML')
    parser.add_argument('-o', dest="outfile", help="CSV output file")
    parser.add_argument('infile', nargs="+", help="WAV file(s)")
    args = parser.parse_args()

    output_fields = ["OriginalFilename", "FileContent", "FileUse", "INAM", "ICRD", "form", "Duration", "language",
                     "ISRC", "xmp_description", "interviewer", "interviewee", "host", "speaker",
                     "performer", "topics", "names", "events", "places", "owner", "ICOP"]

    if args.outfile is not None:
        output = csv.DictWriter(open(args.outfile, 'w'), output_fields)
    else:
        output = csv.DictWriter(sys.stdout, output_fields)

    output.writeheader()
    rows = []

    for infile in args.infile:
        metadata = get_bwf_core(True, infile)
        metadata.update(get_bwf_tech(True, infile))
        metadata.update(get_xmp(infile, ["bwfmetaedit", "--specialchars", "--accept-nopadding"]))
        rows.append({k: metadata[k] for k in output_fields})

    for row in rows:
        output.writerow(row)


if __name__ == '__main__':
    main()
