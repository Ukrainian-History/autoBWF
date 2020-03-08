import sys
import argparse
import re
from autoBWF.BWFfileIO import *


# There is no easy way to write XMP to MP3 without the python-xmp-toolkit and exempi (which was eliminated in v3.1).
# Therefore, the extra tags that were encoded in the earlier versions are now also eliminated.


def construct_command(infile, outfile, metadata, vbr_level):
    command = ["lame", "-V", vbr_level, "--vbr-new"]

    if metadata["INAM"] != "":
        command.extend(['--tv', 'TIT2={}'.format(metadata["INAM"])])
    if metadata["IARL"] != "":
        command.extend(['--tv', "TOWN={}".format(metadata["IARL"])])
    if metadata["ICOP"] != "":
        command.extend(['--tv', "TCOP={}".format(metadata["ICOP"])])
    if metadata["ISRC"] != "":
        command.extend(['--tv', "TIT1={}".format(metadata["ISRC"])])

    if metadata["Description"] != "":
        m = re.search(r'File content: +(.+?);', metadata["Description"])
        if m:
            command.extend(['--tv', "TIT3={}".format(m.group(1))])

    if metadata["ICRD"] != "":
        command.extend(["--ty", metadata["ICRD"]])

    command.extend(['--tv', "TLAN={}".format(metadata["language"])])
    command.extend(["--id3v2-only", infile, outfile])

    return command


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
        if args.outfile is None:
            outfile = infile.rsplit('.', 1)[0] + '.mp3'
        else:
            outfile = args.outfile

        metadata = get_bwf_core(infile)
        metadata.update(get_xmp(infile))
        subprocess.call(construct_command(infile, outfile, metadata, str(args.vbr_level)))


if __name__ == '__main__':
    main()
