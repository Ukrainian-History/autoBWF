import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from main import Ui_autoBWF
import subprocess

class MainWindow(QtWidgets.QDialog, Ui_autoBWF):
    def __init__(self, filename, techMD, config, template, parent=None):
        import re
        # from datetime import date
        from datetime import datetime
        import os.path

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        m = re.compile(config["filenameRegex"]).match(filename)
        if not m: 
            QMessageBox.warning(self, 'Warning', filename + " does not follow filenaming convention")

        matches = m.groups()
        self.identifier = matches[0]
        self.identifier = self.identifier.replace("-", ".")
        self.identifier = self.identifier.replace("_", "")

        self.fileUse = matches[1]
        datestring = matches[2]
        self.datestring_iso = datestring[0:4] + "-" + datestring[4:6] + "-" + datestring[6:]

        date_time = datetime.fromtimestamp(os.path.getctime(filename)).replace(microsecond=0).isoformat()
        [date, time] = date_time.split("T")

        if date != self.datestring_iso:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Filename and timestamp dates disagree")
            msg.setInformativeText("filename: " + self.datestring_iso + "\ntimestamp: " + date)
            msg.setWindowTitle("Choose date")
            msg.addButton('Use ' + self.datestring_iso, QMessageBox.NoRole)
            msg.addButton('Use ' + date, QMessageBox.YesRole)
            retval = msg.exec_()
            if retval == 1:
                self.datestring_iso = date

        self.originationDateLine.insert(self.datestring_iso)
        self.originationTimeLine.insert(time)
        self.originatorRefLine.insert("UkrHECA " + self.datestring_iso.replace("-", "") + " " + time.replace(":", ""))

        try:
            self.fileUse = config["fileuse"][self.fileUse]
        except KeyError:
            print(self.fileUse + " does not not have a standard translation")

        description = "File content: " + self.identifier + "; File use: " + self.fileUse + "; Original filename: " + filename
        self.descriptionLine.insert(description)

        self.originatorLine.insert(config["originator"])

        ###############
        ##### configure dropdowns
        ###############

        self.speedSelect.addItems(config["speed"])
        self.mediaSelect.addItems(config["media"])
        self.eqSelect.addItems(config["eq"])
        self.typeSelect.addItems(config["type"])
        self.technicianBox.addItems(config["technician"])
        self.isftSelect.addItems(config["isft"])
        self.sourceSelect.addItems(config["source"])

        self.deckSelect.addItems(config["deck"]["list"])
        self.adcSelect.addItems(config["adc"]["list"])
        self.softwareSelect.addItems(config["software"]["list"])
        self.copyrightSelect.addItems(config["copyright"]["list"])

        ###############
        ##### set up signals/slots
        ###############

        self.copyrightSelect.activated.connect(self.copyrightActivated)

        self.deckSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.adcSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.softwareSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.mediaSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.speedSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.eqSelect.currentIndexChanged.connect(self.updateCodingHistory)
        self.typeSelect.currentIndexChanged.connect(self.updateCodingHistory)

        self.buttonBox.accepted.connect(self.saveBwf)

        ###############
        ##### prefill defaults and insert existing values
        ###############

        self.updateCodingHistory(0)
        self.copyrightText.insertPlainText(config["copyright"][config["copyright"]["list"][0]])

        self.originalCore = getBwfCore(config["accept-nopadding"], filename)
        if self.originalCore["INAM"] != "": self.insertDefaultLine(self.titleLine, self.originalCore["INAM"])
        if self.originalCore["Description"] != "": self.insertDefaultLine(self.descriptionLine, self.originalCore["Description"])
        if self.originalCore["Originator"] != "": self.insertDefaultLine(self.originatorLine, self.originalCore["Originator"])
        if self.originalCore["OriginatorReference"] != "": self.insertDefaultLine(self.originatorRefLine, self.originalCore["OriginatorReference"])
        if self.originalCore["OriginationDate"] != "": self.insertDefaultLine(self.originationDateLine, self.originalCore["OriginationDate"])
        if self.originalCore["OriginationTime"] != "": self.insertDefaultLine(self.originationTimeLine, self.originalCore["OriginationTime"])
        if self.originalCore["ICRD"] != "": self.insertDefaultLine(self.creationDateLine, self.originalCore["ICRD"])
        if self.originalCore["ITCH"] != "" and (self.originalCore["ITCH"] is not None): self.insertDefaultBox(self.technicianBox, self.originalCore["ITCH"])
        if self.originalCore["ISFT"] != "": self.insertDefaultBox(self.isftSelect, self.originalCore["ISFT"])
        if self.originalCore["ISRC"] != "": self.insertDefaultBox(self.sourceSelect, self.originalCore["ISRC"])
        if self.originalCore["CodingHistory"] != "": self.insertDefaultText(self.codingHistoryText, self.originalCore["CodingHistory"])
        if self.originalCore["ICMT"] != "": self.insertDefaultText(self.commentText, self.originalCore["ICMT"])
        if self.originalCore["ICOP"] != "": self.insertDefaultText(self.copyrightText, self.originalCore["ICOP"])

        if techMD["MD5Stored"] != "": self.md5Check.setEnabled(False)

        ###############
        ##### replace with template values if they exist
        ###############
        
        if template != None:
            core = getBwfCore(config["accept-nopadding"], template)
            if core["INAM"] != "": self.titleLine.insert(core["INAM"])
            if core["ITCH"] != "": self.technicianBox.lineEdit().setText(core["ITCH"])
            if core["CodingHistory"] != "":
                self.codingHistoryText.clear()
                self.codingHistoryText.insertPlainText(core["CodingHistory"])
            if core["ICOP"] != "":
                self.copyrightText.clear()
                self.copyrightText.insertPlainText(core["ICOP"])

    
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

    def updateCodingHistory(self, index):
        deck = self.deckSelect.currentText()
        adc = self.adcSelect.currentText()
        software = self.softwareSelect.currentText()
        media = self.mediaSelect.currentText()
        speed = self.speedSelect.currentText()
        eq = self.eqSelect.currentText()
        type = self.typeSelect.currentText()

        analogprops = [x for x in [config["deck"][deck], media, speed, eq, type] if x != ""]
        channels = {"1": "mono", "2": "stereo"}

        history = "A=ANALOGUE,M=stereo,T=" + "; ".join(analogprops) 
        history += "\r\nA=PCM,F=" + techMD["SampleRate"] + ",W=" + techMD["BitPerSample"] + \
                ",M=stereo,T=" + config["adc"][adc]
        history += "\r\nA=PCM,F=" + techMD["SampleRate"] + ",W=" + techMD["BitPerSample"] + \
                ",M=" + channels[techMD["Channels"]] + ",T=" + config["software"][software] 

        self.codingHistoryText.clear()
        self.codingHistoryText.insertPlainText(history)

    def saveBwf(self):
        command = "bwfmetaedit --specialchars "
        if config["accept-nopadding"]: command += "--accept-nopadding "

        if self.md5Check.isChecked() and self.md5Check.isEnabled():
            sysout = subprocess.call(command + "--MD5-embed " + filename, shell=True)
        
        self.callBwf(command, filename, "Timereference", "0")
        self.callBwf(command, filename, "Description", self.descriptionLine.text())
        self.callBwf(command, filename, "Originator", self.originatorLine.text())
        self.callBwf(command, filename, "OriginatorReference", self.originatorRefLine.text())
        self.callBwf(command, filename, "OriginationDate", self.originationDateLine.text())
        self.callBwf(command, filename, "OriginationTime", self.originationTimeLine.text())
        self.callBwf(command, filename, "ICOP", self.copyrightText.toPlainText())
        self.callBwf(command, filename, "INAM", self.titleLine.text())
        self.callBwf(command, filename, "ITCH", self.technicianBox.currentText())
        self.callBwf(command, filename, "ICMT", self.commentText.toPlainText())
        self.callBwf(command, filename, "ICRD", self.creationDateLine.text())
        self.callBwf(command, filename, "ISFT", self.isftSelect.currentText())
        self.callBwf(command, filename, "ISRC", self.sourceSelect.currentText())
        self.callBwf(command, filename, "History", self.codingHistoryText.toPlainText())
		# for some bizarre reason, --History has to be last, otherwise there's duplication of the last two characters of the history string...

    def callBwf(self, command, filename, key, text):
        # deal with inconsistencies in bwfmetaedit
        if key == "Timereference": 
            mdkey = "TimeReference"
        elif key == "History":
            mdkey = "CodingHistory"
        else:
            mdkey = key

        if text != self.originalCore[mdkey]:
            print("saving " + key)
            print(command + '--' + key + '="' + text + '" ' + filename)
            sysout = subprocess.call(command + '--' + key + '="' + text + '" ' + filename, shell=True)

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
    parser.add_argument('filename', help='WAV file to be processed')
    parser.add_argument('-t', help="template file")
    args = parser.parse_args()
    filename = args.filename
    template = args.t

    techMD = getBwfTech(config["accept-nopadding"], filename)
    if techMD["Errors"] != "":
        sys.exit(1)

    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow(filename, techMD, config, template)
    form.show()

    sys.exit(app.exec_())
