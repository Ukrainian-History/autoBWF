import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from main import Ui_Dialog

config = None

class MainWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

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


    def copyrightActivated(self, index):
        self.copyrightText.clear()
        self.copyrightText.insertPlainText(config["copyright"][config["copyright"]["list"][index]])

    def updateCodingHistory(self, index): 
        dum = "File content: Accession " + acc + " Reel " + reel + ". File use: " + use + ". Original filename: " + file



if __name__ == "__main__":
    import json

    with open('config.json') as data_file:    
        config = json.load(data_file)

    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()

    sys.exit(app.exec_())

