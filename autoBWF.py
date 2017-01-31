import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from main import Ui_Dialog

config = None
filename = ""

class MainWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
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
            msg.setText("Dates in filename and timestamp disagree")
            msg.setInformativeText("filename date: " + self.datestring_iso + ", timestamp date: " + date)
            msg.setWindowTitle("Choose date")
            msg.addButton('Use ' + self.datestring_iso, QMessageBox.NoRole)
            msg.addButton('Use ' + date, QMessageBox.YesRole)
            retval = msg.exec_()
            if retval == 1:
                self.datestring_iso = date

        self.originationDateLine.insert(self.datestring_iso)
        self.originationTimeLine.insert(time)

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

        self.updateCodingHistory(0)
        self.copyrightText.insertPlainText(config["copyright"][config["copyright"]["list"][0]])


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
        history = "A=ANALOGUE,M=stereo,T=" + "; ".join(analogprops) 
        history += "\r\nA=PCM,F=96000,W=24,M=stereo,T=" + config["adc"][adc]
        history += "\r\nA=PCM,F=96000,W=24,M=stereo,T=" + config["software"][software] 
        # need to change 96000, 24, and stereo to whatever is read from tech MD

        self.codingHistoryText.clear()
        self.codingHistoryText.insertPlainText(history)


def getBwfTech(allow_padding):
    import subprocess
    import io
    import csv

    if allow_padding:
        command = "bwfmetaedit --accept-nopadding --out-tech " + filename
    else:
        command = "bwfmetaedit --out-tech " + filename

    tech_csv = subprocess.check_output(command, shell=True, universal_newlines=True)
    f = io.StringIO(tech_csv)
    reader = csv.DictReader(f, delimiter=',')
    tech = next(reader)
    return(tech)


if __name__ == "__main__":
    import json
    import argparse

    with open('config.json') as data_file:    
        config = json.load(data_file)

    parser = argparse.ArgumentParser(description='Create internal metadata for WAV file(s).')
    parser.add_argument('filename', help='WAV file to be processed')
    args = parser.parse_args()
    filename = args.filename

    techMD = getBwfTech(config["accept-nopadding"])
    if techMD["Errors"] != "":
        sys.exit(1)

    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()

    sys.exit(app.exec_())
