import sys
import argparse
import re
import subprocess
import datetime


def parse_line(line):
    edit = None
    fn = re.match(r'\S+\.wav', line, re.I)
    if fn:
        filename = fn[0]
        edit = {"filename": filename}
        line = line.replace(filename, "")

        fade = re.search(r'fade (?P<fadestart>\S+) (?P<fadeend>\S+)', line)
        if fade:
            line = line.replace(fade[0], "")
            edit = {**edit, **fade.groupdict()}  # merge the dicts

        pad = re.search(r'pad (?P<padstart>\S+) (?P<padend>\S+)', line)
        if pad:
            line = line.replace(pad[0], "")
            edit = {**edit, **pad.groupdict()}

        contrast = re.search(r'contrast (?P<contrast>\S+)', line)
        if contrast:
            line = line.replace(contrast[0], "")
            edit = {**edit, **contrast.groupdict()}

        inout = re.search(r'\s*(?P<in>\S+)\s+(?P<out>\S+)', line)
        if inout:
            line = line.replace(inout[0], "")
            edit = {**edit, **inout.groupdict()}

        # at this point, if there's any non-whitespace left, then it's a syntax error

        if re.search(r'\S+', line):
            sys.exit("syntax error in EDL file")

    return edit


def construct_edit(edit):
    out = '"| sox ' + edit["filename"] + ' -t wav - trim ' + edit["in"] + " =" + edit["out"]

    if "fadestart" in edit:
        out += " fade " + edit["fadestart"] + " -0 " + edit["fadeend"]

    if "padstart" in edit:
        out += " pad " + edit["padstart"] + " " + edit["padend"]

    out += '"'
    return out


def finalize(edit, edits):
    command = "sox -V6 " + ' '.join(edits) + " " + edit["filename"]

    if "contrast" in edit:
        command += " contrast " + edit["contrast"]

    return command


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', help="EDL file", type=argparse.FileType('r'))

    args = parser.parse_args()

    edits = list()

    for line in args.infile.readlines():
        edit = parse_line(line)
        if not edit:
            continue

        if "in" in edit:
            edits.append(construct_edit(edit))
        else:
            cmd = finalize(edit, edits)
            outfile = edit["filename"]
            break

    timenow = datetime.datetime.now().replace(microsecond=0).isoformat()
    timenow = timenow.replace(':', '')
    filename = "autosplice" + timenow

    with open(filename + ".cmd", 'w') as output:
        output.write(cmd)

    try:
        soxout = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        exit(
            "You must have SoX v14.4.2 or higher installed on your system to run autosplice.\n"
            "Please download and install the latest version from http://sox.sourceforge.net\n"
            "or using your package manager.")

    with open(filename + ".out", 'wb') as output:
        output.write(soxout.stderr)

    subprocess.call("bwfmetaedit --specialchars --MD5-embed " + outfile, shell=True)
    subprocess.run("bwfmetaedit --specialchars --ICMT='" + cmd + "' " + outfile, shell=True)

    try:
        version = subprocess.check_output('sox --version', shell=True).decode("utf-8")
    except subprocess.CalledProcessError:
        exit(
            "You must have SoX v14.4.2 or higher installed on your system to run autosplice.\n"
            "Please download and install the latest version from http://sox.sourceforge.net\n"
            "or using your package manager.")

    version = re.sub(r'^sox: +', '', version)
    subprocess.run('bwfmetaedit --specialchars --ISFT="' + version + '" ' + outfile, shell=True)


if __name__ == '__main__':
    main()
