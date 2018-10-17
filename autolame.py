import sys
import argparse
import subprocess
import re
from BWFfileIO import *


def main(arguments):
    from libxmp import XMPFiles, consts

    parser = argparse.ArgumentParser(
        description='Use lame to create mp3 file from BWF, using BWF metadata to populate IDv2 tags')
    parser.add_argument('infile', help="WAV file")
    parser.add_argument('outfile', help="MP3 file")
    parser.add_argument('--vbr-level', help="MP3 VBR encoding level", type=int, default=7)
    args = parser.parse_args(arguments)

    command = ["lame", "-V", str(args.vbr_level),  "--vbr-new"]

    bwf_metadata = get_bwf_core(True, args.infile)
    xmp_metadata = get_xmp(args.infile, ["bwfmetaedit", "--specialchars", "--accept-nopadding"])

    if bwf_metadata["INAM"] != "":
        command.append('--tv "TIT2={}" '.format(bwf_metadata["INAM"]))
    if bwf_metadata["IARL"] != "":
        command.append('--tv "TOWN={}" '.format(bwf_metadata["IARL"]))
    if bwf_metadata["ICOP"] != "":
        command.append('--tv "TCOP={}" '.format(bwf_metadata["ICOP"]))
    if bwf_metadata["ISRC"] != "":
        command.append('--tv "TIT1={}" '.format(bwf_metadata["ISRC"]))

    if bwf_metadata["Description"] != "":
        m = re.search(r'File content: +(.+?);', bwf_metadata["Description"])
        if m:
            command.append('--tv "TIT3={}" '.format(m.group(1)))

    if bwf_metadata["ICRD"] != "":
        command.append('--ty "{}" '.format(bwf_metadata["ICRD"]))

    command.append('--tv "TLAN={}" '.format(xmp_metadata["language"]))
    command.extend(["--id3v2-only", args.infile, args.outfile])
    subprocess.call(command)

    # xmpfile = XMPFiles(file_path=args.outfile, open_forupdate=True)
    # xmp = xmpfile.get_xmp()
    #
    # if xmp_metadata["owner"]:
    #     xmp.set_localized_text(
    #         consts.XMP_NS_XMP_Rights, 'Owner',
    #         'en', 'en-US', xmp_metadata["owner"])
    # if xmp_metadata["description"]:
    #     xmp.set_localized_text(
    #         consts.XMP_NS_DC, 'description',
    #         'en', 'en-US', xmp_metadata["description"])
    #
    # if xmp_metadata["language"]:
    #     for lang in xmp_metadata["language"].split(";"):
    #         xmp.append_array_item(consts.XMP_NS_DC, 'language',
    #                               lang.strip(),
    #                               {'prop_array_is_ordered': False,
    #                                'prop_value_is_array': True})
    #
    # xmp.register_namespace(autobwf_ns, 'autoBWF')
    #
    # if xmp_metadata["interviewer"]:
    #     xmp.set_localized_text(
    #         autobwf_ns, 'Interviewer',
    #         'en', 'en-US', xmp_metadata["interviewer"])
    # if xmp_metadata["interviewee"]:
    #     xmp.set_localized_text(
    #         autobwf_ns, 'Interviewee',
    #         'en', 'en-US', xmp_metadata["interviewee"])
    #
    # if xmp_metadata["metadataDate"]:
    #     xmp.set_property_datetime(
    #         consts.XMP_NS_XMP, 'MetadataDate',
    #         xmp_metadata["metadataDate"])
    #
    # xmpfile.put_xmp(xmp)
    # xmpfile.close_file()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
