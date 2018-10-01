import subprocess


def call_bwf(command, file, key, text):
        # deal with annoying inconsistencies in bwfmetaedit
        if key == "Timereference":
            mdkey = "TimeReference"
        elif key == "History":
            mdkey = "CodingHistory"
        else:
            mdkey = key

        if text != self.original_md[mdkey]:
            subprocess.call(command + '--' + key + '="' + text + '" ' + file, shell=True)

def get_bwf_tech(allow_padding, file):
    import io
    import csv

    if allow_padding:
        command = "bwfmetaedit --accept-nopadding --out-tech " + file
    else:
        command = "bwfmetaedit --out-tech " + file

    tech_csv = subprocess.check_output(command, shell=True, universal_newlines=True)
    f = io.StringIO(tech_csv)
    reader = csv.DictReader(f, delimiter=',')
    tech = next(reader)
    return tech


def get_bwf_core(allow_padding, file):
    import io
    import csv

    if allow_padding:
        command = "bwfmetaedit --accept-nopadding --out-core " + file
    else:
        command = "bwfmetaedit --out-core " + file

    core_csv = subprocess.check_output(command, shell=True, universal_newlines=True)
    f = io.StringIO(core_csv)
    reader = csv.DictReader(f, delimiter=',')
    core = next(reader)
    return core