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
        if os.path.isfile(args.outfile):
            # if file exists, assume that it is a bwf2csv output file, append rows without generating header
            output = csv.DictWriter(open(args.outfile, 'a'), output_fields)
        else:
            # otherwise, create new file and generate header
            output = csv.DictWriter(open(args.outfile, 'w'), output_fields)
            output.writeheader()
    else:
        output = csv.DictWriter(sys.stdout, output_fields)
        output.writeheader()

    for infile in args.infile:
        metadata = get_bwf_core(True, infile)
        metadata.update(get_bwf_tech(True, infile))
        metadata.update(get_xmp(infile, ["bwfmetaedit", "--specialchars", "--accept-nopadding"]))
        output.writerow({k: metadata[k] for k in output_fields})


if __name__ == '__main__':
    main()
