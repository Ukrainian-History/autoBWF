import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from tabbed import Ui_autoBWF
import subprocess


class MainWindow(QtWidgets.QMainWindow, Ui_autoBWF):
    def __init__(self, filename, config, template, parent=None):
        self.autobwf_ns_short = None
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

        self.copyrightSelect.activated.connect(self.copyrightActivated)
        self.deckSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.adcSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.softwareSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.mediaSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.speedSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.eqSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.typeSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.actionUpdate_metadata.triggered.connect(self.saveBwf)
        self.actionQuit.triggered.connect(self.close)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionOpen_template.connect(self.openTemplate)

        self.tabWidget.setEnabled(False)
        self.actionUpdate_metadata.setEnabled(False)

        if filename:
            self.tabWidget.setEnabled(True)
            self.actionUpdate_metadata.setEnabled(True)
            self.populateFileInfo(filename)

        if template:
            self.populateTemplateInfo(template)

    def openFile(self):
        fname = str(QFileDialog.getOpenFileName(self, "Open Wave file", "~")[0])
        if fname:
            # check to make sure file is legit
            md = getBwfTech(config["accept-nopadding"], fname)
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
                self.populateFileInfo(fname)

        self.filename = fname

    def openTemplate(self):
        fname = str(QFileDialog.getOpenFileName(self, "Open template file", "~")[0])
        if fname:
            # check to make sure file is legit
            md = getBwfTech(config["accept-nopadding"], fname)
            if md["Errors"] != "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(fname + " does not appear to be a valid Wave file")
                msg.exec_()
            else:
                self.actionOpen_template.setEnabled(False)
                self.populateTemplateInfo(fname)

    def populateFileInfo(self, file):
        import re
        import os.path
        from datetime import datetime

        techMD = getBwfTech(config["accept-nopadding"], file)

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
                "; Original filename: " + file
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

        self.updateCodingHistory(0, techMD)

        #
        # prefill defaults and insert existing values
        #

        self.originalCore = getBwfCore(config["accept-nopadding"], file)

        if self.originalCore["INAM"] != "":
            self.insertDefaultLine(self.titleLine, self.originalCore["INAM"])
        if self.originalCore["Description"] != "":
            self.insertDefaultLine(self.descriptionLine, self.originalCore["Description"])
        if self.originalCore["Originator"] != "":
            self.insertDefaultLine(self.originatorLine, self.originalCore["Originator"])
        if self.originalCore["OriginatorReference"] != "":
            self.insertDefaultLine(self.originatorRefLine, self.originalCore["OriginatorReference"])
        if self.originalCore["OriginationDate"] != "":
            self.insertDefaultLine(self.originationDateLine, self.originalCore["OriginationDate"])
        if self.originalCore["OriginationTime"] != "":
            self.insertDefaultLine(self.originationTimeLine, self.originalCore["OriginationTime"])
        if self.originalCore["ICRD"] != "":
            self.insertDefaultLine(self.creationDateLine, self.originalCore["ICRD"])
        if self.originalCore["ITCH"] != "" and (self.originalCore["ITCH"] is not None):
            self.insertDefaultBox(self.technicianBox, self.originalCore["ITCH"])
        if self.originalCore["ISFT"] != "":
            self.insertDefaultBox(self.isftSelect, self.originalCore["ISFT"])
        if self.originalCore["ISRC"] != "":
            self.insertDefaultBox(self.sourceSelect, self.originalCore["ISRC"])
        if self.originalCore["CodingHistory"] != "":
            self.insertDefaultText(self.codingHistoryText, self.originalCore["CodingHistory"])
        if self.originalCore["ICMT"] != "":
            self.insertDefaultText(self.commentText, self.originalCore["ICMT"])
        if self.originalCore["ICOP"] != "":
            self.insertDefaultText(self.copyrightText, self.originalCore["ICOP"])

        if techMD["MD5Stored"] != "":
            self.md5Check.setEnabled(False)

        self.originalXmp = self.getXmp(file)
        if self.originalXmp["description"] != "":
            self.insertDefaultText(self.descriptionText, self.originalXmp["description"])
        if self.originalXmp["owner"] != "":
            self.insertDefaultBox(self.rightsOwnerSelect, self.originalXmp["owner"])
        if self.originalXmp["language"] != "":
            self.insertDefaultLine(self.languageLine, self.originalXmp["language"])
        if self.originalXmp["interviewer"] != "":
            self.insertDefaultLine(self.interviewerLine, self.originalXmp["interviewer"])
        if self.originalXmp["interviewee"] != "":
            self.insertDefaultLine(self.intervieweeLine, self.originalXmp["interviewee"])

    def populateTemplateInfo(self, file):
        # replace with template values if they exist

        if file is not None:
            core = getBwfCore(config["accept-nopadding"], file)
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

            templateXmp = self.getXmp(file)
            if templateXmp["description"] != "":
                self.insertDefaultText(self.descriptionText, templateXmp["description"])
            if templateXmp["owner"] != "":
                self.insertDefaultBox(self.rightsOwnerSelect, templateXmp["owner"])
            if templateXmp["language"] != "":
                self.insertDefaultLine(self.languageLine, templateXmp["language"])
            if templateXmp["interviewer"] != "":
                self.insertDefaultLine(self.interviewerLine, templateXmp["interviewer"])
            if templateXmp["interviewee"] != "":
                self.insertDefaultLine(self.intervieweeLine, templateXmp["interviewee"])

    def insertDefaultLine(self, widget, text):
        widget.clear()
        widget.insert(text)
        widget.setStyleSheet("color: grey; font: italic")
        widget.textChanged.connect(lambda: self.activateChanged(widget))

    def insertDefaultBox(self, widget, text):
        widget.setCurrentText(text)
        widget.setStyleSheet("color: grey; font: italic")
        widget.currentTextChanged.connect(lambda: self.activateChanged(widget))

    def insertDefaultText(self, widget, text):
        widget.clear()
        widget.insertPlainText(text)
        widget.setStyleSheet("color: grey; font: italic")
        widget.textChanged.connect(lambda: self.activateChanged(widget))

    def activateChanged(self, inputWidget):
        inputWidget.setStyleSheet("color: red; font: normal")

    def copyrightActivated(self, index):
        self.copyrightText.clear()
        self.copyrightText.insertPlainText(config["copyright"][config["copyright"]["list"][index]])

    def updateCodingHistory(self, index, techMD):
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
            "\r\nA=PCM,F=", techMD["SampleRate"],
            ",W=", techMD["BitPerSample"],
            ",M=stereo,T=", config["adc"][adc],
            "\r\nA=PCM,F=", techMD["SampleRate"],
            ",W=" + techMD["BitPerSample"],
            ",M=" + channels[techMD["Channels"]],
            ",T=" + config["software"][software]
        ]

        history = "".join(history_list)
        self.codingHistoryText.clear()
        self.codingHistoryText.insertPlainText(history)

    def getXmp(self, file):
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

            try:
                xmp_dict["language"] = xmp.get_localized_text(
                    libxmp.consts.XMP_NS_DC, 'language', 'en', 'en-US')
            except libxmp.XMPError:
                pass

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

    def saveBwf(self):
        from libxmp import XMPFiles, consts

        # first the BWF and RIFF
        command = "bwfmetaedit --specialchars "
        if config["accept-nopadding"]:
            command += "--accept-nopadding "

        if self.md5Check.isChecked() and self.md5Check.isEnabled():
            sysout = subprocess.call(command + "--MD5-embed " + self.filename, shell=True)

        self.callBwf(command, self.filename, "Timereference", "0")
        self.callBwf(command, self.filename, "Description", self.descriptionLine.text())
        self.callBwf(command, self.filename, "Originator", self.originatorLine.text())
        self.callBwf(command, self.filename, "OriginatorReference", self.originatorRefLine.text())
        self.callBwf(command, self.filename, "OriginationDate", self.originationDateLine.text())
        self.callBwf(command, self.filename, "OriginationTime", self.originationTimeLine.text())
        self.callBwf(command, self.filename, "ICOP", self.copyrightText.toPlainText())
        self.callBwf(command, self.filename, "INAM", self.titleLine.text())
        self.callBwf(command, self.filename, "ITCH", self.technicianBox.currentText())
        self.callBwf(command, self.filename, "ICMT", self.commentText.toPlainText())
        self.callBwf(command, self.filename, "ICRD", self.creationDateLine.text())
        self.callBwf(command, self.filename, "ISFT", self.isftSelect.currentText())
        self.callBwf(command, self.filename, "ISRC", self.sourceSelect.currentText())
        self.callBwf(command, self.filename, "IARL", config["iarl"])
        self.callBwf(command, self.filename, "History", self.codingHistoryText.toPlainText())
        # for some bizarre reason, --History has to be last,
        # otherwise there's duplication of the last two characters of the history string...

        # XMP must be done after RIFF, as xmp library crashes if wav has no RIFF tags
        xmpfile = XMPFiles(file_path=self.filename, open_forupdate=True)
        xmp = xmpfile.get_xmp()

        xmp.set_localized_text(
            consts.XMP_NS_XMP_Rights, 'Owner',
            'en', 'en-US', self.rightsOwnerSelect.currentText())
        xmp.set_localized_text(
            consts.XMP_NS_DC, 'description',
            'en', 'en-US', self.descriptionText.toPlainText())
        xmp.set_localized_text(
            consts.XMP_NS_DC, 'language',
            'en', 'en-US', self.languageLine.text())

        if not self.autobwf_ns_short:
            self.autobwf_ns_short = xmp.register_namespace(self.autobwf_ns, 'autoBWF')

        xmp.set_localized_text(
            self.autobwf_ns, 'Interviewer',
            'en', 'en-US', self.interviewerLine.text())
        xmp.set_localized_text(
            self.autobwf_ns, 'Interviewee',
            'en', 'en-US', self.intervieweeLine.text())

        xmpfile.put_xmp(xmp)
        xmpfile.close_file()

    def callBwf(self, command, file, key, text):
        # deal with annoying inconsistencies in bwfmetaedit
        if key == "Timereference":
            mdkey = "TimeReference"
        elif key == "History":
            mdkey = "CodingHistory"
        else:
            mdkey = key

        if text != self.originalCore[mdkey]:
            sysout = subprocess.call(command + '--' + key + '="' + text + '" ' + file, shell=True)


def getBwfTech(allow_padding, file):
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


def getBwfCore(allow_padding, file):
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
        techMD = getBwfTech(config["accept-nopadding"], filename)
        if techMD["Errors"] != "":
            print(filename + " does not appear to be a valid Wave file")
            sys.exit(1)

    if template:
        # check to make sure file is legit
        dum = getBwfTech(config["accept-nopadding"], template)
        if dum["Errors"] != "":
            print(template + " does not appear to be a valid Wave file")
            sys.exit(1)

    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow(filename, config, template)
    form.show()

    sys.exit(app.exec_())
