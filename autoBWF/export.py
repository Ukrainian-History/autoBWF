# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export.ui'
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
        self.lineEdit = QtWidgets.QLineEdit(Export)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Export)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(Export)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(Export)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Export)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(Export)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 2, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(Export)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(Export)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Export)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 1, 1, 2)

        self.retranslateUi(Export)
        self.buttonBox.accepted.connect(Export.accept)
        self.buttonBox.rejected.connect(Export.reject)
        QtCore.QMetaObject.connectSlotsByName(Export)

    def retranslateUi(self, Export):
        _translate = QtCore.QCoreApplication.translate
        Export.setWindowTitle(_translate("Export", "Dialog"))
        self.label.setText(_translate("Export", "Destination PBCore"))
        self.pushButton.setText(_translate("Export", "Select"))
        self.checkBox.setText(_translate("Export", "Include OHMS file"))
        self.pushButton_2.setText(_translate("Export", "Select"))
        self.checkBox_2.setText(_translate("Export", "Generate MP3"))
        self.pushButton_3.setText(_translate("Export", "Select"))


