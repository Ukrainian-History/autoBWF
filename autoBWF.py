import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from tabbed import Ui_autoBWF
import subprocess


class MainWindow(QtWidgets.QMainWindow, Ui_autoBWF):
    def __init__(self, filename, config, template, parent=None):
        self.autobwf_ns = "http://ns.ukrhec.org/autoBWF/0.1"

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.filename = filename

        #
        # configure dropdowns and texts
        #

        self.originatorLine.insert(config["originator"])
        self.speedSelect.addItems(config["speed"])
        self.mediaSelect.addItems(config["media"])
        self.eqSelect.addItems(config["eq"])
        self.typeSelect.addItems(config["type"])
        self.technicianBox.addItems(config["technician"])
        self.isftSelect.addItems(config["isft"])
        self.sourceSelect.addItems(config["source"])
        self.rightsOwnerSelect.addItems(config["owner"])
        self.deckSelect.addItems(config["deck"]["list"])
        self.adcSelect.addItems(config["adc"]["list"])
        self.softwareSelect.addItems(config["software"]["list"])
        self.copyrightSelect.addItems(config["copyright"]["list"])
        self.copyrightText.insertPlainText(
            config["copyright"][config["copyright"]["list"][0]]
        )

        #
        # set up signals/slots
        #

        self.copyrightSelect.activated.connect(self.copyright_activated)
        self.deckSelect.currentIndexChanged.connect(self.update_coding_history)
        self.adcSelect.currentIndexChanged.connect(self.update_coding_history)
        self.softwareSelect.currentIndexChanged.connect(self.update_coding_history)
        self.mediaSelect.currentIndexChanged.connect(self.update_coding_history)
        self.speedSelect.currentIndexChanged.connect(self.update_coding_history)
        self.eqSelect.currentIndexChanged.connect(self.update_coding_history)
        self.typeSelect.currentIndexChanged.connect(self.update_coding_history)
        self.actionUpdate_metadata.triggered.connect(self.save_metadata)
        self.actionQuit.triggered.connect(self.close)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionOpen_template.triggered.connect(self.open_template)

        self.tabWidget.setEnabled(False)
        self.actionUpdate_metadata.setEnabled(False)
        self.actionOpen_template.setEnabled(False)

        if filename:
            self.tabWidget.setEnabled(True)
            self.actionUpdate_metadata.setEnabled(True)
            self.actionOpen.setEnabled(False)
            self.populate_file_info(filename)

        if template:
            self.populate_template_info(template)

    def open_file(self):
        fname = str(QFileDialog.getOpenFileName(self, "Open Wave file", "~")[0])
        if fname:
            # check to make sure file is legit
            md = get_bwf_tech(config["accept-nopadding"], fname)
            if md["Errors"] != "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(fname + " does not appear to be a valid Wave file")
                msg.exec_()
            else:
                self.tabWidget.setEnabled(True)
                self.actionUpdate_metadata.setEnabled(True)
                self.actionOpen_template.setEnabled(True)
                self.actionOpen.setEnabled(False)
                self.populate_file_info(fname)

        self.filename = fname

    def open_template(self):
        fname = str(QFileDialog.getOpenFileName(self, "Open template file", "~")[0])
        if fname:
            # check to make sure file is legit
            md = get_bwf_tech(config["accept-nopadding"], fname)
            if md["Errors"] != "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(fname + " does not appear to be a valid Wave file")
                msg.exec_()
            else:
                self.actionOpen_template.setEnabled(False)
                self.populate_template_info(fname)

    def populate_file_info(self, file):
        import re
        import os.path
        from datetime import datetime

        self.tech_md = get_bwf_tech(config["accept-nopadding"], file)

        date_time = datetime \
            .fromtimestamp(os.path.getctime(file)) \
            .replace(microsecond=0) \
            .isoformat()
        [date, time] = date_time.split("T")

        m = re.compile(config["filenameRegex"]).match(file)
        if m:
            matches = m.groups()
            self.identifier = matches[0]
            self.identifier = self.identifier.replace("-", ".")
            self.identifier = self.identifier.replace("_", "")

            self.fileUse = matches[1]
            datestring = matches[2]
            self.datestring_iso = (
                datestring[0:4] + "-" +
                datestring[4:6] + "-" +
                datestring[6:]
            )

            if date != self.datestring_iso:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Filename and timestamp dates disagree")
                msg.setInformativeText(
                    "filename: " + self.datestring_iso +
                    "\ntimestamp: " + date)
                msg.setWindowTitle("Choose date")
                msg.addButton('Use ' + self.datestring_iso, QMessageBox.NoRole)
                msg.addButton('Use ' + date, QMessageBox.YesRole)
                retval = msg.exec_()
                if retval == 1:
                    self.datestring_iso = date

            self.originationDateLine.insert(self.datestring_iso)
            self.originationTimeLine.insert(time)
            self.originatorRefLine.insert(
                config["repocode"] + " " +
                self.datestring_iso.replace("-", "") + " " +
                time.replace(":", ""))

            try:
                self.fileUse = config["fileuse"][self.fileUse]
            except KeyError:
                print(
                    self.fileUse +
                    " does not not have a standard translation"
                )
                self.fileUse = "Unknown"

            description = (
                "File content: " + self.identifier +
                "; File use: " + self.fileUse +
                "; Original filename: " + os.path.basename(file)
            )
            self.descriptionLine.insert(description)
        else:
            QMessageBox.warning(
                self, 'Warning',
                file + " does not follow filenaming convention"
            )
            self.originationDateLine.insert(date)
            self.originationTimeLine.insert(time)
            self.originatorRefLine.insert(
                config["repocode"] + " " +
                date.replace("-", "") + " " +
                time.replace(":", "")
            )

        self.update_coding_history()

        #
        # prefill defaults and insert existing values
        #

        self.originalCore = get_bwf_core(config["accept-nopadding"], file)

        if self.originalCore["INAM"] != "":
            self.insert_default_line(self.titleLine, self.originalCore["INAM"])
        if self.originalCore["Description"] != "":
            self.insert_default_line(self.descriptionLine, self.originalCore["Description"])
        if self.originalCore["Originator"] != "":
            self.insert_default_line(self.originatorLine, self.originalCore["Originator"])
        if self.originalCore["OriginatorReference"] != "":
            self.insert_default_line(self.originatorRefLine, self.originalCore["OriginatorReference"])
        if self.originalCore["OriginationDate"] != "":
            self.insert_default_line(self.originationDateLine, self.originalCore["OriginationDate"])
        if self.originalCore["OriginationTime"] != "":
            self.insert_default_line(self.originationTimeLine, self.originalCore["OriginationTime"])
        if self.originalCore["ICRD"] != "":
            self.insert_default_line(self.creationDateLine, self.originalCore["ICRD"])
        if self.originalCore["ITCH"] != "" and (self.originalCore["ITCH"] is not None):
            self.insert_default_box(self.technicianBox, self.originalCore["ITCH"])
        if self.originalCore["ISFT"] != "":
            self.insert_default_box(self.isftSelect, self.originalCore["ISFT"])
        if self.originalCore["ISRC"] != "":
            self.insert_default_box(self.sourceSelect, self.originalCore["ISRC"])
        if self.originalCore["CodingHistory"] != "":
            self.insert_default_text(self.codingHistoryText, self.originalCore["CodingHistory"])
        if self.originalCore["ICMT"] != "":
            self.insert_default_text(self.commentText, self.originalCore["ICMT"])
        if self.originalCore["ICOP"] != "":
            self.insert_default_text(self.copyrightText, self.originalCore["ICOP"])

        if self.tech_md["MD5Stored"] != "":
            self.md5Check.setEnabled(False)

        self.originalXmp = self.get_xmp(file)
        if self.originalXmp["description"] != "":
            self.insert_default_text(self.descriptionText, self.originalXmp["description"])
        if self.originalXmp["owner"] != "":
            self.insert_default_box(self.rightsOwnerSelect, self.originalXmp["owner"])
        if self.originalXmp["language"] != "":
            self.insert_default_line(self.languageLine, self.originalXmp["language"])
        if self.originalXmp["interviewer"] != "":
            self.insert_default_line(self.interviewerLine, self.originalXmp["interviewer"])
        if self.originalXmp["interviewee"] != "":
            self.insert_default_line(self.intervieweeLine, self.originalXmp["interviewee"])

    def populate_template_info(self, file):
        # replace with template values if they exist

        if file is not None:
            core = get_bwf_core(config["accept-nopadding"], file)
            if core["INAM"] != "":
                self.titleLine.clear()
                self.titleLine.insert(core["INAM"])
            if core["ISRC"] != "":
                self.sourceSelect.lineEdit().setText(core["ISRC"])
            if core["ITCH"] != "" and (self.originalCore["ITCH"] is not None):
                self.technicianBox.lineEdit().setText(core["ITCH"])
            if core["CodingHistory"] != "":
                self.codingHistoryText.clear()
                self.codingHistoryText.insertPlainText(core["CodingHistory"])
            if core["ICOP"] != "":
                self.copyrightText.clear()
                self.copyrightText.insertPlainText(core["ICOP"])

            template_xmp = self.get_xmp(file)
            if template_xmp["description"] != "":
                self.insert_default_text(self.descriptionText, template_xmp["description"])
            if template_xmp["owner"] != "":
                self.insert_default_box(self.rightsOwnerSelect, template_xmp["owner"])
            if template_xmp["language"] != "":
                self.insert_default_line(self.languageLine, template_xmp["language"])
            if template_xmp["interviewer"] != "":
                self.insert_default_line(self.interviewerLine, template_xmp["interviewer"])
            if template_xmp["interviewee"] != "":
                self.insert_default_line(self.intervieweeLine, template_xmp["interviewee"])

    def insert_default_line(self, widget, text):
        widget.clear()
        widget.insert(text)
        widget.setStyleSheet("color: grey; font: italic")
        widget.textChanged.connect(lambda: self.activate_changed(widget))

    def insert_default_box(self, widget, text):
        widget.setCurrentText(text)
        widget.setStyleSheet("color: grey; font: italic")
        widget.currentTextChanged.connect(lambda: self.activate_changed(widget))

    def insert_default_text(self, widget, text):
        widget.clear()
        widget.insertPlainText(text)
        widget.setStyleSheet("color: grey; font: italic")
        widget.textChanged.connect(lambda: self.activate_changed(widget))

    def activate_changed(self, input_widget):
        input_widget.setStyleSheet("color: red; font: normal")

    def copyright_activated(self, index):
        self.copyrightText.clear()
        self.copyrightText.insertPlainText(config["copyright"][config["copyright"]["list"][index]])

    def update_coding_history(self):
        deck = self.deckSelect.currentText()
        adc = self.adcSelect.currentText()
        software = self.softwareSelect.currentText()
        media = self.mediaSelect.currentText()
        speed = self.speedSelect.currentText()
        eq = self.eqSelect.currentText()
        type = self.typeSelect.currentText()

        analogprops = [x for x in [config["deck"][deck], media, speed, eq, type] if x != ""]
        channels = {"1": "mono", "2": "stereo"}

        history_list = [
            "A=ANALOGUE,M=stereo,T=", "; ".join(analogprops),
            "\r\nA=PCM,F=", self.tech_md["SampleRate"],
            ",W=", self.tech_md["BitPerSample"],
            ",M=stereo,T=", config["adc"][adc],
            "\r\nA=PCM,F=", self.tech_md["SampleRate"],
            ",W=" + self.tech_md["BitPerSample"],
            ",M=" + channels[self.tech_md["Channels"]],
            ",T=" + config["software"][software]
        ]

        history = "".join(history_list)
        self.codingHistoryText.clear()
        self.codingHistoryText.insertPlainText(history)

    def get_xmp(self, file):
        import libxmp

        xmpfile = libxmp.XMPFiles(file_path=file, open_forupdate=False)
        xmp = xmpfile.get_xmp()
        xmp_dict = {"owner": "", "description": "", "language": "",
                    "interviewer": "", "interviewee": ""}

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

            xmp.register_namespace(self.autobwf_ns, 'autoBWF')

            try:
                xmp_dict["interviewer"] = xmp.get_localized_text(
                    self.autobwf_ns, 'Interviewer', 'en', 'en-US')
            except libxmp.XMPError:
                pass

            try:
                xmp_dict["interviewee"] = xmp.get_localized_text(
                    self.autobwf_ns, 'Interviewee', 'en', 'en-US')
            except libxmp.XMPError:
                pass

        return xmp_dict

    def save_metadata(self):
        from libxmp import XMPFiles, consts
        from datetime import datetime

        # first the BWF and RIFF
        command = "bwfmetaedit --specialchars "
        if config["accept-nopadding"]:
            command += "--accept-nopadding "

        if self.md5Check.isChecked() and self.md5Check.isEnabled():
            subprocess.call(command + "--MD5-embed " + self.filename, shell=True)

        self.call_bwf(command, self.filename, "Timereference", "0")
        self.call_bwf(command, self.filename, "Description", self.descriptionLine.text())
        self.call_bwf(command, self.filename, "Originator", self.originatorLine.text())
        self.call_bwf(command, self.filename, "OriginatorReference", self.originatorRefLine.text())
        self.call_bwf(command, self.filename, "OriginationDate", self.originationDateLine.text())
        self.call_bwf(command, self.filename, "OriginationTime", self.originationTimeLine.text())
        self.call_bwf(command, self.filename, "ICOP", self.copyrightText.toPlainText())
        self.call_bwf(command, self.filename, "INAM", self.titleLine.text())
        self.call_bwf(command, self.filename, "ITCH", self.technicianBox.currentText())
        self.call_bwf(command, self.filename, "ICMT", self.commentText.toPlainText())
        self.call_bwf(command, self.filename, "ICRD", self.creationDateLine.text())
        self.call_bwf(command, self.filename, "ISFT", self.isftSelect.currentText())
        self.call_bwf(command, self.filename, "ISRC", self.sourceSelect.currentText())
        self.call_bwf(command, self.filename, "IARL", config["iarl"])
        self.call_bwf(command, self.filename, "History", self.codingHistoryText.toPlainText())
        # for some bizarre reason, --History has to be last,
        # otherwise there's duplication of the last two characters of the history string...

        # XMP must be done after RIFF, as xmp library crashes if wav has no RIFF tags
        xmpfile = XMPFiles(file_path=self.filename, open_forupdate=True)
        xmp = xmpfile.get_xmp()

        if self.rightsOwnerSelect.currentText():
            xmp.set_localized_text(
                consts.XMP_NS_XMP_Rights, 'Owner',
                'en', 'en-US', self.rightsOwnerSelect.currentText())
        if self.descriptionText.toPlainText():
            xmp.set_localized_text(
                consts.XMP_NS_DC, 'description',
                'en', 'en-US', self.descriptionText.toPlainText())

        if self.languageLine.text():
            # delete languages first to prevent appending to existing array
            xmp.delete_property(consts.XMP_NS_DC, 'language')

            for lang in self.languageLine.text().split(";"):
                xmp.append_array_item(consts.XMP_NS_DC, 'language',
                                      lang.strip(),
                                      {'prop_array_is_ordered': False,
                                       'prop_value_is_array': True})

        xmp.register_namespace(self.autobwf_ns, 'autoBWF')

        if self.interviewerLine.text():
            xmp.set_localized_text(
                self.autobwf_ns, 'Interviewer',
                'en', 'en-US', self.interviewerLine.text())
        if self.intervieweeLine.text():
            xmp.set_localized_text(
                self.autobwf_ns, 'Interviewee',
                'en', 'en-US', self.intervieweeLine.text())

        xmp.set_property_datetime(consts.XMP_NS_XMP,
                                  "MetadataDate", datetime.now())

        xmpfile.put_xmp(xmp)
        xmpfile.close_file()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Metadata saved successfully")
        msg.exec_()

    def call_bwf(self, command, file, key, text):
        # deal with annoying inconsistencies in bwfmetaedit
        if key == "Timereference":
            mdkey = "TimeReference"
        elif key == "History":
            mdkey = "CodingHistory"
        else:
            mdkey = key

        if text != self.originalCore[mdkey]:
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
    return(tech)


def get_bwf_core(allow_padding, file):
    import io
    import csv

    if allow_padding:
        command = "bwfmetaedit --accept-nopadding --out-core " + file
    else:
        command = "bwfmetaedit --out-core " + file

    tech_csv = subprocess.check_output(command, shell=True, universal_newlines=True)
    f = io.StringIO(tech_csv)
    reader = csv.DictReader(f, delimiter=',')
    tech = next(reader)
    return(tech)


if __name__ == "__main__":
    import json
    import argparse
    import inspect

    path = inspect.stack()[0][1]
    path = path.replace("autoBWF.py", "config.json")

    with open(path) as data_file:
        config = json.load(data_file)

    parser = argparse.ArgumentParser(description='Create internal metadata for WAV file(s).')
    parser.add_argument('filename', nargs='?', help='WAV file to be processed')
    parser.add_argument('-t', help="template file")
    args = parser.parse_args()
    filename = args.filename
    template = args.t

    if filename:
        # check to make sure file is legit
        techMD = get_bwf_tech(config["accept-nopadding"], filename)
        if techMD["Errors"] != "":
            print(filename + " does not appear to be a valid Wave file")
            sys.exit(1)

    if template:
        # check to make sure file is legit
        dum = get_bwf_tech(config["accept-nopadding"], template)
        if dum["Errors"] != "":
            print(template + " does not appear to be a valid Wave file")
            sys.exit(1)

    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow(filename, config, template)
    form.show()

    sys.exit(app.exec_())
