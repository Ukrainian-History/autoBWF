# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Export(object):
    def setupUi(self, Export):
        Export.setObjectName("Export")
        Export.resize(679, 212)
        self.gridLayout = QtWidgets.QGridLayout(Export)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Export)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.outFile = QtWidgets.QLineEdit(Export)
        self.outFile.setObjectName("outFile")
        self.gridLayout.addWidget(self.outFile, 0, 1, 1, 3)
        self.outfileButton = QtWidgets.QPushButton(Export)
        self.outfileButton.setObjectName("outfileButton")
        self.gridLayout.addWidget(self.outfileButton, 0, 4, 1, 1)
        self.ohmsCheck = QtWidgets.QCheckBox(Export)
        self.ohmsCheck.setObjectName("ohmsCheck")
        self.gridLayout.addWidget(self.ohmsCheck, 1, 0, 1, 1)
        self.ohmsFile = QtWidgets.QLineEdit(Export)
        self.ohmsFile.setObjectName("ohmsFile")
        self.gridLayout.addWidget(self.ohmsFile, 1, 1, 1, 3)
        self.ohmsfileButton = QtWidgets.QPushButton(Export)
        self.ohmsfileButton.setObjectName("ohmsfileButton")
        self.gridLayout.addWidget(self.ohmsfileButton, 1, 4, 1, 1)
        self.lameCheck = QtWidgets.QCheckBox(Export)
        self.lameCheck.setObjectName("lameCheck")
        self.gridLayout.addWidget(self.lameCheck, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Export)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.vbrLevel = QtWidgets.QSpinBox(Export)
        self.vbrLevel.setMaximum(9)
        self.vbrLevel.setProperty("value", 7)
        self.vbrLevel.setObjectName("vbrLevel")
        self.gridLayout.addWidget(self.vbrLevel, 2, 2, 1, 1)
        self.mp3File = QtWidgets.QLineEdit(Export)
        self.mp3File.setObjectName("mp3File")
        self.gridLayout.addWidget(self.mp3File, 2, 3, 1, 1)
        self.mp3fileButton = QtWidgets.QPushButton(Export)
        self.mp3fileButton.setObjectName("mp3fileButton")
        self.gridLayout.addWidget(self.mp3fileButton, 2, 4, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Export)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 3, 1, 2)

        self.retranslateUi(Export)
        self.buttonBox.accepted.connect(Export.accept)
        self.buttonBox.rejected.connect(Export.reject)
        QtCore.QMetaObject.connectSlotsByName(Export)

    def retranslateUi(self, Export):
        _translate = QtCore.QCoreApplication.translate
        Export.setWindowTitle(_translate("Export", "Dialog"))
        self.label.setText(_translate("Export", "Destination PBCore"))
        self.outfileButton.setText(_translate("Export", "Select"))
        self.ohmsCheck.setText(_translate("Export", "Embed XML"))
        self.ohmsfileButton.setText(_translate("Export", "Select"))
        self.lameCheck.setText(_translate("Export", "Generate MP3"))
        self.label_2.setText(_translate("Export", "VBR level"))
        self.mp3fileButton.setText(_translate("Export", "Select"))


