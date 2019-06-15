import sys
import argparse
import re
from autoBWF.BWFfileIO import *


def main():
    parser = argparse.ArgumentParser(
        description='Use lame to create mp3 file from BWF, using BWF metadata to populate IDv2 tags')
    parser.add_argument('-o', dest="outfile", help="MP3 file")
    parser.add_argument('--vbr-level', help="MP3 VBR encoding level", type=int, default=7)
    parser.add_argument('infile', nargs="+", help="WAV file")
    args = parser.parse_args()

    if args.outfile is not None and len(args.infile) > 1:
        sys.exit("Can only have one input file if output file is specified.")

    for infile in args.infile:
        command = ["lame", "-V", str(args.vbr_level), "--vbr-new"]

        if args.outfile is None:
            outfile = infile.rsplit('.', 1)[0] + '.mp3'
        else:
            outfile = args.outfile

        bwf_metadata = get_bwf_core(True, infile)
        xmp_metadata = get_xmp(infile, ["bwfmetaedit", "--specialchars", "--accept-nopadding"])

        if bwf_metadata["INAM"] != "":
            command.extend(['--tv', 'TIT2={}'.format(bwf_metadata["INAM"])])
        if bwf_metadata["IARL"] != "":
            command.extend(['--tv', "TOWN={}".format(bwf_metadata["IARL"])])
        if bwf_metadata["ICOP"] != "":
            command.extend(['--tv', "TCOP={}".format(bwf_metadata["ICOP"])])
        if bwf_metadata["ISRC"] != "":
            command.extend(['--tv', "TIT1={}".format(bwf_metadata["ISRC"])])

        if bwf_metadata["Description"] != "":
            m = re.search(r'File content: +(.+?);', bwf_metadata["Description"])
            if m:
                command.extend(['--tv', "TIT3={}".format(m.group(1))])

        if bwf_metadata["ICRD"] != "":
            command.extend(["--ty", bwf_metadata["ICRD"]])

        command.extend(['--tv', "TLAN={}".format(xmp_metadata["language"])])
        command.extend(["--id3v2-only", infile, outfile])
        subprocess.call(command)

    # no easy way to write XMP to MP3 without the python-xmp-toolkit and exempi (which has been eliminated), so
    # we're eliminating the extra tags that were encoded in the earlier versions


if __name__ == '__main__':
    main()
