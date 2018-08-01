import sys
import argparse
import subprocess
import re

autobwf_ns = "http://ns.ukrhec.org/autoBWF/0.1"


def get_bwf_core(file):
    import io
    import csv

    command = "bwfmetaedit --accept-nopadding --out-core " + file

    tech_csv = subprocess.check_output(command, shell=True, universal_newlines=True)
    f = io.StringIO(tech_csv)
    reader = csv.DictReader(f, delimiter=',')
    tech = next(reader)
    return tech


def get_xmp(file):
    import libxmp

    xmpfile = libxmp.XMPFiles(file_path=file, open_forupdate=False)
    xmp = xmpfile.get_xmp()
    xmp_dict = {"owner": "", "description": "", "language": "",
                "interviewer": "", "interviewee": "", "metadataDate": ""}

    if xmp:
        try:
            xmp_dict["owner"] = xmp.get_localized_text(
                libxmp.consts.XMP_NS_XMP_Rights, 'Owner', 'en', 'en-US')
        except libxmp.XMPError:
            pass

        try:
            xmp_dict["description"] = xmp.get_localized_text(
                libxmp.consts.XMP_NS_DC, 'description', 'en', 'en-US')
        except libxmp.XMPError:
            pass

        languages = []
        i = 1
        while True:
            try:
                languages.append(xmp.get_array_item(
                    libxmp.consts.XMP_NS_DC, 'language', i))
            except libxmp.XMPError:
                xmp_dict["language"] = ";".join(languages)
                break

            i += 1

        xmp.register_namespace(autobwf_ns, 'autoBWF')

        try:
            xmp_dict["interviewer"] = xmp.get_localized_text(
                autobwf_ns, 'Interviewer', 'en', 'en-US')
        except libxmp.XMPError:
            pass

        try:
            xmp_dict["interviewee"] = xmp.get_localized_text(
                autobwf_ns, 'Interviewee', 'en', 'en-US')
        except libxmp.XMPError:
            pass

        try:
            xmp_dict["metadataDate"] = xmp.get_property_datetime(libxmp.consts.XMP_NS_XMP,
                                                                 "MetadataDate")
        except libxmp.XMPError:
            pass

    return xmp_dict

def main(arguments):
    from libxmp import XMPFiles, consts

    parser = argparse.ArgumentParser(
        description='Use lame to create mp3 file from BWF, using BWF metadata to populate IDv2 tags')
    parser.add_argument('infile', help="WAV file")
    parser.add_argument('outfile', help="MP3 file")
    parser.add_argument('--vbr-level', help="MP3 VBR encoding level", type=int, default=6)
    args = parser.parse_args(arguments)

    command = "lame -V {} --vbr-new ".format(args.vbr_level)

    bwf_metadata = get_bwf_core(args.infile)
    xmp_metadata = get_xmp(args.infile)

    if bwf_metadata["INAM"] != "":
        command += '--tv "TIT2={}" '.format(bwf_metadata["INAM"])
    if bwf_metadata["IARL"] != "":
        command += '--tv "TOWN={}" '.format(bwf_metadata["IARL"])
    if bwf_metadata["ICOP"] != "":
        command += '--tv "TCOP={}" '.format(bwf_metadata["ICOP"])
    if bwf_metadata["ISRC"] != "":
        command += '--tv "TIT1={}" '.format(bwf_metadata["ISRC"])

    if bwf_metadata["Description"] != "":
        m = re.search(r'File content: +(.+?);', bwf_metadata["Description"])
        if m:
            command += '--tv "TIT3={}" '.format(m.group(1))

    if bwf_metadata["ICRD"] != "":
        command += '--ty "{}" '.format(bwf_metadata["ICRD"])

    command += '--tv "TLAN={}" '.format(xmp_metadata["language"])
    command += "--id3v2-only {} {}".format(args.infile, args.outfile)
    subprocess.call(command, shell=True)

    xmpfile = XMPFiles(file_path=args.outfile, open_forupdate=True)
    xmp = xmpfile.get_xmp()

    if xmp_metadata["owner"]:
        xmp.set_localized_text(
            consts.XMP_NS_XMP_Rights, 'Owner',
            'en', 'en-US', xmp_metadata["owner"])
    if xmp_metadata["description"]:
        xmp.set_localized_text(
            consts.XMP_NS_DC, 'description',
            'en', 'en-US', xmp_metadata["description"])

    if xmp_metadata["language"]:
        for lang in xmp_metadata["language"].split(";"):
            xmp.append_array_item(consts.XMP_NS_DC, 'language',
                                  lang.strip(),
                                  {'prop_array_is_ordered': False,
                                   'prop_value_is_array': True})

    xmp.register_namespace(autobwf_ns, 'autoBWF')

    if xmp_metadata["interviewer"]:
        xmp.set_localized_text(
            autobwf_ns, 'Interviewer',
            'en', 'en-US', xmp_metadata["interviewer"])
    if xmp_metadata["interviewee"]:
        xmp.set_localized_text(
            autobwf_ns, 'Interviewee',
            'en', 'en-US', xmp_metadata["interviewee"])

    if xmp_metadata["metadataDate"]:
        xmp.set_property_datetime(
            consts.XMP_NS_XMP, 'MetadataDate',
            xmp_metadata["metadataDate"])

    xmpfile.put_xmp(xmp)
    xmpfile.close_file()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
