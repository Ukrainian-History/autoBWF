# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabbed.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_autoBWF(object):
    def setupUi(self, autoBWF):
        autoBWF.setObjectName("autoBWF")
        autoBWF.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(autoBWF)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.bwfTab = QtWidgets.QWidget()
        self.bwfTab.setObjectName("bwfTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.bwfTab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_7.setObjectName("formLayout_7")
        self.descriptionLabel = QtWidgets.QLabel(self.bwfTab)
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.descriptionLabel)
        self.descriptionLine = QtWidgets.QLineEdit(self.bwfTab)
        self.descriptionLine.setObjectName("descriptionLine")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.descriptionLine)
        self.horizontalLayout.addLayout(self.formLayout_7)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.originatorLabel = QtWidgets.QLabel(self.bwfTab)
        self.originatorLabel.setObjectName("originatorLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.originatorLabel)
        self.originatorLine = QtWidgets.QLineEdit(self.bwfTab)
        self.originatorLine.setObjectName("originatorLine")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.originatorLine)
        self.horizontalLayout_3.addLayout(self.formLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.originatorRefLine = QtWidgets.QLineEdit(self.bwfTab)
        self.originatorRefLine.setObjectName("originatorRefLine")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.originatorRefLine)
        self.originatorRefLabel = QtWidgets.QLabel(self.bwfTab)
        self.originatorRefLabel.setObjectName("originatorRefLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.originatorRefLabel)
        self.horizontalLayout_4.addLayout(self.formLayout_2)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_3.setObjectName("formLayout_3")
        self.originationDateLine = QtWidgets.QLineEdit(self.bwfTab)
        self.originationDateLine.setObjectName("originationDateLine")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.originationDateLine)
        self.originationDateLabel = QtWidgets.QLabel(self.bwfTab)
        self.originationDateLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.originationDateLabel.setObjectName("originationDateLabel")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.originationDateLabel)
        self.horizontalLayout_5.addLayout(self.formLayout_3)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_4.setObjectName("formLayout_4")
        self.originationTimeLabel = QtWidgets.QLabel(self.bwfTab)
        self.originationTimeLabel.setObjectName("originationTimeLabel")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.originationTimeLabel)
        self.originationTimeLine = QtWidgets.QLineEdit(self.bwfTab)
        self.originationTimeLine.setObjectName("originationTimeLine")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.originationTimeLine)
        self.horizontalLayout_6.addLayout(self.formLayout_4)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 2, 1, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.formLayout_9 = QtWidgets.QFormLayout()
        self.formLayout_9.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_9.setObjectName("formLayout_9")
        self.codingHistoryLabel = QtWidgets.QLabel(self.bwfTab)
        self.codingHistoryLabel.setObjectName("codingHistoryLabel")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.codingHistoryLabel)
        self.codingHistoryText = QtWidgets.QPlainTextEdit(self.bwfTab)
        self.codingHistoryText.setObjectName("codingHistoryText")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.codingHistoryText)
        self.horizontalLayout_10.addLayout(self.formLayout_9)
        self.gridLayout_3.addLayout(self.horizontalLayout_10, 3, 0, 1, 2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.deckSelect = QtWidgets.QComboBox(self.bwfTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deckSelect.sizePolicy().hasHeightForWidth())
        self.deckSelect.setSizePolicy(sizePolicy)
        self.deckSelect.setEditable(False)
        self.deckSelect.setObjectName("deckSelect")
        self.gridLayout_2.addWidget(self.deckSelect, 0, 0, 1, 1)
        self.softwareSelect = QtWidgets.QComboBox(self.bwfTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.softwareSelect.sizePolicy().hasHeightForWidth())
        self.softwareSelect.setSizePolicy(sizePolicy)
        self.softwareSelect.setEditable(False)
        self.softwareSelect.setObjectName("softwareSelect")
        self.gridLayout_2.addWidget(self.softwareSelect, 0, 1, 1, 2)
        self.adcSelect = QtWidgets.QComboBox(self.bwfTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.adcSelect.sizePolicy().hasHeightForWidth())
        self.adcSelect.setSizePolicy(sizePolicy)
        self.adcSelect.setEditable(False)
        self.adcSelect.setObjectName("adcSelect")
        self.gridLayout_2.addWidget(self.adcSelect, 1, 0, 1, 1)
        self.mediaSelect = QtWidgets.QComboBox(self.bwfTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mediaSelect.sizePolicy().hasHeightForWidth())
        self.mediaSelect.setSizePolicy(sizePolicy)
        self.mediaSelect.setEditable(False)
        self.mediaSelect.setObjectName("mediaSelect")
        self.gridLayout_2.addWidget(self.mediaSelect, 1, 1, 1, 2)
        self.formLayout_12 = QtWidgets.QFormLayout()
        self.formLayout_12.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_12.setObjectName("formLayout_12")
        self.label_13 = QtWidgets.QLabel(self.bwfTab)
        self.label_13.setObjectName("label_13")
        self.formLayout_12.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.typeSelect = QtWidgets.QComboBox(self.bwfTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.typeSelect.sizePolicy().hasHeightForWidth())
        self.typeSelect.setSizePolicy(sizePolicy)
        self.typeSelect.setEditable(False)
        self.typeSelect.setObjectName("typeSelect")
        self.formLayout_12.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.typeSelect)
        self.gridLayout_2.addLayout(self.formLayout_12, 2, 0, 1, 3)
        self.formLayout_11 = QtWidgets.QFormLayout()
        self.formLayout_11.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_11.setObjectName("formLayout_11")
        self.label_12 = QtWidgets.QLabel(self.bwfTab)
        self.label_12.setObjectName("label_12")
        self.formLayout_11.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.eqSelect = QtWidgets.QComboBox(self.bwfTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eqSelect.sizePolicy().hasHeightForWidth())
        self.eqSelect.setSizePolicy(sizePolicy)
        self.eqSelect.setEditable(False)
        self.eqSelect.setObjectName("eqSelect")
        self.formLayout_11.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.eqSelect)
        self.gridLayout_2.addLayout(self.formLayout_11, 3, 0, 1, 2)
        self.formLayout_10 = QtWidgets.QFormLayout()
        self.formLayout_10.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_10.setObjectName("formLayout_10")
        self.label_7 = QtWidgets.QLabel(self.bwfTab)
        self.label_7.setObjectName("label_7")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.speedSelect = QtWidgets.QComboBox(self.bwfTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speedSelect.sizePolicy().hasHeightForWidth())
        self.speedSelect.setSizePolicy(sizePolicy)
        self.speedSelect.setEditable(False)
        self.speedSelect.setObjectName("speedSelect")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.speedSelect)
        self.gridLayout_2.addLayout(self.formLayout_10, 3, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 4, 0, 1, 2)
        self.md5Check = QtWidgets.QCheckBox(self.bwfTab)
        self.md5Check.setChecked(True)
        self.md5Check.setObjectName("md5Check")
        self.gridLayout_3.addWidget(self.md5Check, 5, 0, 1, 2)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.bwfTab, "")
        self.riffTab = QtWidgets.QWidget()
        self.riffTab.setObjectName("riffTab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.riffTab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_5.setObjectName("formLayout_5")
        self.titleLabel = QtWidgets.QLabel(self.riffTab)
        self.titleLabel.setObjectName("titleLabel")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.titleLabel)
        self.titleLine = QtWidgets.QLineEdit(self.riffTab)
        self.titleLine.setObjectName("titleLine")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.titleLine)
        self.horizontalLayout_7.addLayout(self.formLayout_5)
        self.gridLayout_5.addLayout(self.horizontalLayout_7, 0, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.creationDateLabel = QtWidgets.QLabel(self.riffTab)
        self.creationDateLabel.setObjectName("creationDateLabel")
        self.horizontalLayout_2.addWidget(self.creationDateLabel)
        self.creationDateLine = QtWidgets.QLineEdit(self.riffTab)
        self.creationDateLine.setObjectName("creationDateLine")
        self.horizontalLayout_2.addWidget(self.creationDateLine)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.formLayout_13 = QtWidgets.QFormLayout()
        self.formLayout_13.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_13.setObjectName("formLayout_13")
        self.commentLabel = QtWidgets.QLabel(self.riffTab)
        self.commentLabel.setObjectName("commentLabel")
        self.formLayout_13.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.commentLabel)
        self.commentText = QtWidgets.QPlainTextEdit(self.riffTab)
        self.commentText.setObjectName("commentText")
        self.formLayout_13.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.commentText)
        self.horizontalLayout_11.addLayout(self.formLayout_13)
        self.gridLayout_5.addLayout(self.horizontalLayout_11, 1, 1, 4, 1)
        self.formLayout_17 = QtWidgets.QFormLayout()
        self.formLayout_17.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_17.setObjectName("formLayout_17")
        self.sourceLabel = QtWidgets.QLabel(self.riffTab)
        self.sourceLabel.setObjectName("sourceLabel")
        self.formLayout_17.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.sourceLabel)
        self.sourceSelect = QtWidgets.QComboBox(self.riffTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sourceSelect.sizePolicy().hasHeightForWidth())
        self.sourceSelect.setSizePolicy(sizePolicy)
        self.sourceSelect.setEditable(True)
        self.sourceSelect.setObjectName("sourceSelect")
        self.formLayout_17.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.sourceSelect)
        self.gridLayout_5.addLayout(self.formLayout_17, 2, 0, 1, 1)
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_6.setObjectName("formLayout_6")
        self.technicianLabel = QtWidgets.QLabel(self.riffTab)
        self.technicianLabel.setObjectName("technicianLabel")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.technicianLabel)
        self.technicianBox = QtWidgets.QComboBox(self.riffTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.technicianBox.sizePolicy().hasHeightForWidth())
        self.technicianBox.setSizePolicy(sizePolicy)
        self.technicianBox.setEditable(True)
        self.technicianBox.setObjectName("technicianBox")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.technicianBox)
        self.gridLayout_5.addLayout(self.formLayout_6, 3, 0, 1, 1)
        self.formLayout_14 = QtWidgets.QFormLayout()
        self.formLayout_14.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_14.setObjectName("formLayout_14")
        self.isftLabel = QtWidgets.QLabel(self.riffTab)
        self.isftLabel.setObjectName("isftLabel")
        self.formLayout_14.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.isftLabel)
        self.isftSelect = QtWidgets.QComboBox(self.riffTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.isftSelect.sizePolicy().hasHeightForWidth())
        self.isftSelect.setSizePolicy(sizePolicy)
        self.isftSelect.setEditable(True)
        self.isftSelect.setObjectName("isftSelect")
        self.formLayout_14.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.isftSelect)
        self.gridLayout_5.addLayout(self.formLayout_14, 4, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.formLayout_8 = QtWidgets.QFormLayout()
        self.formLayout_8.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_8.setObjectName("formLayout_8")
        self.copyrightLabel = QtWidgets.QLabel(self.riffTab)
        self.copyrightLabel.setObjectName("copyrightLabel")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.copyrightLabel)
        self.copyrightText = QtWidgets.QPlainTextEdit(self.riffTab)
        self.copyrightText.setObjectName("copyrightText")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.copyrightText)
        self.horizontalLayout_9.addLayout(self.formLayout_8)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_10 = QtWidgets.QLabel(self.riffTab)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.copyrightSelect = QtWidgets.QComboBox(self.riffTab)
        self.copyrightSelect.setObjectName("copyrightSelect")
        self.verticalLayout.addWidget(self.copyrightSelect)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_9.addLayout(self.verticalLayout)
        self.gridLayout_5.addLayout(self.horizontalLayout_9, 5, 0, 1, 2)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.riffTab, "")
        self.xmpTab = QtWidgets.QWidget()
        self.xmpTab.setObjectName("xmpTab")
        self.layoutWidget_9 = QtWidgets.QWidget(self.xmpTab)
        self.layoutWidget_9.setGeometry(QtCore.QRect(5, 12, 258, 245))
        self.layoutWidget_9.setObjectName("layoutWidget_9")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_9)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget_9)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.description_list = QtWidgets.QListWidget(self.layoutWidget_9)
        self.description_list.setObjectName("description_list")
        self.verticalLayout_2.addWidget(self.description_list)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.description_addbutton = QtWidgets.QToolButton(self.layoutWidget_9)
        self.description_addbutton.setObjectName("description_addbutton")
        self.horizontalLayout_8.addWidget(self.description_addbutton)
        self.description_removebutton = QtWidgets.QToolButton(self.layoutWidget_9)
        self.description_removebutton.setEnabled(False)
        self.description_removebutton.setObjectName("description_removebutton")
        self.horizontalLayout_8.addWidget(self.description_removebutton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.layoutWidget_10 = QtWidgets.QWidget(self.xmpTab)
        self.layoutWidget_10.setGeometry(QtCore.QRect(293, 11, 258, 246))
        self.layoutWidget_10.setObjectName("layoutWidget_10")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget_10)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget_10)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_5.addWidget(self.label_8)
        self.language_list = QtWidgets.QListWidget(self.layoutWidget_10)
        self.language_list.setObjectName("language_list")
        self.verticalLayout_5.addWidget(self.language_list)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.language_choice = QtWidgets.QComboBox(self.layoutWidget_10)
        self.language_choice.setObjectName("language_choice")
        self.horizontalLayout_12.addWidget(self.language_choice)
        self.language_addbutton = QtWidgets.QToolButton(self.layoutWidget_10)
        self.language_addbutton.setObjectName("language_addbutton")
        self.horizontalLayout_12.addWidget(self.language_addbutton)
        self.language_removebutton = QtWidgets.QToolButton(self.layoutWidget_10)
        self.language_removebutton.setEnabled(False)
        self.language_removebutton.setObjectName("language_removebutton")
        self.horizontalLayout_12.addWidget(self.language_removebutton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_12)
        self.layoutWidget_11 = QtWidgets.QWidget(self.xmpTab)
        self.layoutWidget_11.setGeometry(QtCore.QRect(575, 11, 258, 245))
        self.layoutWidget_11.setObjectName("layoutWidget_11")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.layoutWidget_11)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_14 = QtWidgets.QLabel(self.layoutWidget_11)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_14.addWidget(self.label_14)
        self.rights_list = QtWidgets.QListWidget(self.layoutWidget_11)
        self.rights_list.setObjectName("rights_list")
        self.verticalLayout_14.addWidget(self.rights_list)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.rights_addbutton = QtWidgets.QToolButton(self.layoutWidget_11)
        self.rights_addbutton.setObjectName("rights_addbutton")
        self.horizontalLayout_13.addWidget(self.rights_addbutton)
        self.rights_removebutton = QtWidgets.QToolButton(self.layoutWidget_11)
        self.rights_removebutton.setEnabled(False)
        self.rights_removebutton.setObjectName("rights_removebutton")
        self.horizontalLayout_13.addWidget(self.rights_removebutton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem2)
        self.verticalLayout_14.addLayout(self.horizontalLayout_13)
        self.layoutWidget_12 = QtWidgets.QWidget(self.xmpTab)
        self.layoutWidget_12.setGeometry(QtCore.QRect(10, 287, 258, 245))
        self.layoutWidget_12.setObjectName("layoutWidget_12")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget_12)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget_12)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_7.addWidget(self.label_9)
        self.creator_list = QtWidgets.QListWidget(self.layoutWidget_12)
        self.creator_list.setObjectName("creator_list")
        self.verticalLayout_7.addWidget(self.creator_list)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.creator_addbutton = QtWidgets.QToolButton(self.layoutWidget_12)
        self.creator_addbutton.setObjectName("creator_addbutton")
        self.horizontalLayout_14.addWidget(self.creator_addbutton)
        self.creator_removebutton = QtWidgets.QToolButton(self.layoutWidget_12)
        self.creator_removebutton.setEnabled(False)
        self.creator_removebutton.setObjectName("creator_removebutton")
        self.horizontalLayout_14.addWidget(self.creator_removebutton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_14)
        self.layoutWidget_13 = QtWidgets.QWidget(self.xmpTab)
        self.layoutWidget_13.setGeometry(QtCore.QRect(298, 289, 258, 245))
        self.layoutWidget_13.setObjectName("layoutWidget_13")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget_13)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget_13)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6)
        self.contributor_list = QtWidgets.QListWidget(self.layoutWidget_13)
        self.contributor_list.setObjectName("contributor_list")
        self.verticalLayout_4.addWidget(self.contributor_list)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.contributor_addbutton = QtWidgets.QToolButton(self.layoutWidget_13)
        self.contributor_addbutton.setObjectName("contributor_addbutton")
        self.horizontalLayout_15.addWidget(self.contributor_addbutton)
        self.contributor_removebutton = QtWidgets.QToolButton(self.layoutWidget_13)
        self.contributor_removebutton.setEnabled(False)
        self.contributor_removebutton.setObjectName("contributor_removebutton")
        self.horizontalLayout_15.addWidget(self.contributor_removebutton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_15)
        self.layoutWidget_14 = QtWidgets.QWidget(self.xmpTab)
        self.layoutWidget_14.setGeometry(QtCore.QRect(584, 289, 258, 245))
        self.layoutWidget_14.setObjectName("layoutWidget_14")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.layoutWidget_14)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_11 = QtWidgets.QLabel(self.layoutWidget_14)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_8.addWidget(self.label_11)
        self.publisher_list = QtWidgets.QListWidget(self.layoutWidget_14)
        self.publisher_list.setObjectName("publisher_list")
        self.verticalLayout_8.addWidget(self.publisher_list)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.publisher_addbutton = QtWidgets.QToolButton(self.layoutWidget_14)
        self.publisher_addbutton.setObjectName("publisher_addbutton")
        self.horizontalLayout_16.addWidget(self.publisher_addbutton)
        self.publisher_removebutton = QtWidgets.QToolButton(self.layoutWidget_14)
        self.publisher_removebutton.setEnabled(False)
        self.publisher_removebutton.setObjectName("publisher_removebutton")
        self.horizontalLayout_16.addWidget(self.publisher_removebutton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem5)
        self.verticalLayout_8.addLayout(self.horizontalLayout_16)
        self.tabWidget.addTab(self.xmpTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        autoBWF.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(autoBWF)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuOpen = QtWidgets.QMenu(self.menubar)
        self.menuOpen.setObjectName("menuOpen")
        autoBWF.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(autoBWF)
        self.statusbar.setObjectName("statusbar")
        autoBWF.setStatusBar(self.statusbar)
        self.actionUpdate_metadata = QtWidgets.QAction(autoBWF)
        self.actionUpdate_metadata.setObjectName("actionUpdate_metadata")
        self.actionOpen = QtWidgets.QAction(autoBWF)
        self.actionOpen.setObjectName("actionOpen")
        self.actionQuit = QtWidgets.QAction(autoBWF)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpen_template = QtWidgets.QAction(autoBWF)
        self.actionOpen_template.setObjectName("actionOpen_template")
        self.menuOpen.addAction(self.actionOpen)
        self.menuOpen.addAction(self.actionOpen_template)
        self.menuOpen.addAction(self.actionUpdate_metadata)
        self.menuOpen.addAction(self.actionQuit)
        self.menubar.addAction(self.menuOpen.menuAction())

        self.retranslateUi(autoBWF)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(autoBWF)

    def retranslateUi(self, autoBWF):
        _translate = QtCore.QCoreApplication.translate
        autoBWF.setWindowTitle(_translate("autoBWF", "MainWindow"))
        self.descriptionLabel.setText(_translate("autoBWF", "Description"))
        self.originatorLabel.setText(_translate("autoBWF", "Originator"))
        self.originatorRefLabel.setText(_translate("autoBWF", "OriginatorRef"))
        self.originationDateLabel.setText(_translate("autoBWF", "OriginationDate"))
        self.originationTimeLabel.setText(_translate("autoBWF", "OriginationTime"))
        self.codingHistoryLabel.setText(_translate("autoBWF", "CodingHistory"))
        self.label_13.setText(_translate("autoBWF", "Tape type"))
        self.label_12.setText(_translate("autoBWF", "EQ"))
        self.label_7.setText(_translate("autoBWF", "Speed"))
        self.md5Check.setText(_translate("autoBWF", "Embed MD5 of data chunk"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bwfTab), _translate("autoBWF", "BWF"))
        self.titleLabel.setText(_translate("autoBWF", "Title"))
        self.creationDateLabel.setText(_translate("autoBWF", "Creation Date"))
        self.commentLabel.setText(_translate("autoBWF", "Comment"))
        self.sourceLabel.setText(_translate("autoBWF", "Source"))
        self.technicianLabel.setText(_translate("autoBWF", "Technician"))
        self.isftLabel.setText(_translate("autoBWF", "ISFT"))
        self.copyrightLabel.setText(_translate("autoBWF", "Copyright"))
        self.label_10.setText(_translate("autoBWF", "Replace with boilerplate:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.riffTab), _translate("autoBWF", "RIFF"))
        self.label_3.setText(_translate("autoBWF", "Description:"))
        self.description_addbutton.setText(_translate("autoBWF", "Add"))
        self.description_removebutton.setText(_translate("autoBWF", "Remove"))
        self.label_8.setText(_translate("autoBWF", "Language:"))
        self.language_addbutton.setText(_translate("autoBWF", "Add"))
        self.language_removebutton.setText(_translate("autoBWF", "Remove"))
        self.label_14.setText(_translate("autoBWF", "Rights Summary:"))
        self.rights_addbutton.setText(_translate("autoBWF", "Add"))
        self.rights_removebutton.setText(_translate("autoBWF", "Remove"))
        self.label_9.setText(_translate("autoBWF", "Creator:"))
        self.creator_addbutton.setText(_translate("autoBWF", "Add"))
        self.creator_removebutton.setText(_translate("autoBWF", "Remove"))
        self.label_6.setText(_translate("autoBWF", "Contributor:"))
        self.contributor_addbutton.setText(_translate("autoBWF", "Add"))
        self.contributor_removebutton.setText(_translate("autoBWF", "Remove"))
        self.label_11.setText(_translate("autoBWF", "Publisher:"))
        self.publisher_addbutton.setText(_translate("autoBWF", "Add"))
        self.publisher_removebutton.setText(_translate("autoBWF", "Remove"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.xmpTab), _translate("autoBWF", "XMP"))
        self.menuOpen.setTitle(_translate("autoBWF", "File"))
        self.actionUpdate_metadata.setText(_translate("autoBWF", "Update metadata"))
        self.actionOpen.setText(_translate("autoBWF", "Open..."))
        self.actionQuit.setText(_translate("autoBWF", "Quit"))
        self.actionOpen_template.setText(_translate("autoBWF", "Open template..."))

