# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabbed.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_autoBWF(object):
    def setupUi(self, autoBWF):
        autoBWF.setObjectName("autoBWF")
        autoBWF.resize(1026, 600)
        self.centralwidget = QtWidgets.QWidget(autoBWF)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.tabWidget = QtWidgets.QTabWidget(self.page)
        self.tabWidget.setObjectName("tabWidget")
        self.bwfTab = QtWidgets.QWidget()
        self.bwfTab.setObjectName("bwfTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.bwfTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
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
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 3)
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
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
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
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)
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
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)
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
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 2, 1, 1, 1)
        self.md5Check = QtWidgets.QCheckBox(self.bwfTab)
        self.md5Check.setChecked(True)
        self.md5Check.setObjectName("md5Check")
        self.gridLayout_2.addWidget(self.md5Check, 3, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.bwfTab)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 4, 0, 1, 3)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.codingHistoryLabel = QtWidgets.QLabel(self.bwfTab)
        self.codingHistoryLabel.setObjectName("codingHistoryLabel")
        self.gridLayout.addWidget(self.codingHistoryLabel, 0, 0, 1, 1)
        self.codingHistoryText = QtWidgets.QPlainTextEdit(self.bwfTab)
        self.codingHistoryText.setObjectName("codingHistoryText")
        self.gridLayout.addWidget(self.codingHistoryText, 0, 1, 2, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 198, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 5, 0, 7, 2)
        self.deckSelect = QtWidgets.QComboBox(self.bwfTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deckSelect.sizePolicy().hasHeightForWidth())
        self.deckSelect.setSizePolicy(sizePolicy)
        self.deckSelect.setEditable(False)
        self.deckSelect.setObjectName("deckSelect")
        self.gridLayout_2.addWidget(self.deckSelect, 5, 2, 1, 1)
        self.softwareSelect = QtWidgets.QComboBox(self.bwfTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.softwareSelect.sizePolicy().hasHeightForWidth())
        self.softwareSelect.setSizePolicy(sizePolicy)
        self.softwareSelect.setEditable(False)
        self.softwareSelect.setObjectName("softwareSelect")
        self.gridLayout_2.addWidget(self.softwareSelect, 6, 2, 1, 1)
        self.adcSelect = QtWidgets.QComboBox(self.bwfTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.adcSelect.sizePolicy().hasHeightForWidth())
        self.adcSelect.setSizePolicy(sizePolicy)
        self.adcSelect.setEditable(False)
        self.adcSelect.setObjectName("adcSelect")
        self.gridLayout_2.addWidget(self.adcSelect, 7, 2, 1, 1)
        self.mediaSelect = QtWidgets.QComboBox(self.bwfTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mediaSelect.sizePolicy().hasHeightForWidth())
        self.mediaSelect.setSizePolicy(sizePolicy)
        self.mediaSelect.setEditable(False)
        self.mediaSelect.setObjectName("mediaSelect")
        self.gridLayout_2.addWidget(self.mediaSelect, 8, 2, 1, 1)
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
        self.gridLayout_2.addLayout(self.formLayout_10, 9, 2, 1, 1)
        self.formLayout_12 = QtWidgets.QFormLayout()
        self.formLayout_12.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_12.setObjectName("formLayout_12")
        self.typeSelect = QtWidgets.QComboBox(self.bwfTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.typeSelect.sizePolicy().hasHeightForWidth())
        self.typeSelect.setSizePolicy(sizePolicy)
        self.typeSelect.setEditable(False)
        self.typeSelect.setObjectName("typeSelect")
        self.formLayout_12.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.typeSelect)
        self.label_13 = QtWidgets.QLabel(self.bwfTab)
        self.label_13.setObjectName("label_13")
        self.formLayout_12.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.gridLayout_2.addLayout(self.formLayout_12, 10, 2, 1, 1)
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
        self.gridLayout_2.addLayout(self.formLayout_11, 11, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
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
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_9.addLayout(self.verticalLayout)
        self.gridLayout_5.addLayout(self.horizontalLayout_9, 5, 0, 1, 2)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.riffTab, "")
        self.xmpTab = QtWidgets.QWidget()
        self.xmpTab.setObjectName("xmpTab")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.xmpTab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.creationDateLabel_2 = QtWidgets.QLabel(self.xmpTab)
        self.creationDateLabel_2.setObjectName("creationDateLabel_2")
        self.horizontalLayout_8.addWidget(self.creationDateLabel_2)
        self.languageLine = QtWidgets.QLineEdit(self.xmpTab)
        self.languageLine.setObjectName("languageLine")
        self.horizontalLayout_8.addWidget(self.languageLine)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.formLayout_18 = QtWidgets.QFormLayout()
        self.formLayout_18.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_18.setObjectName("formLayout_18")
        self.sourceLabel_2 = QtWidgets.QLabel(self.xmpTab)
        self.sourceLabel_2.setObjectName("sourceLabel_2")
        self.formLayout_18.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.sourceLabel_2)
        self.rightsOwnerSelect = QtWidgets.QComboBox(self.xmpTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rightsOwnerSelect.sizePolicy().hasHeightForWidth())
        self.rightsOwnerSelect.setSizePolicy(sizePolicy)
        self.rightsOwnerSelect.setEditable(True)
        self.rightsOwnerSelect.setObjectName("rightsOwnerSelect")
        self.formLayout_18.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.rightsOwnerSelect)
        self.verticalLayout_2.addLayout(self.formLayout_18)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.creationDateLabel_4 = QtWidgets.QLabel(self.xmpTab)
        self.creationDateLabel_4.setObjectName("creationDateLabel_4")
        self.horizontalLayout_13.addWidget(self.creationDateLabel_4)
        self.interviewerLine = QtWidgets.QLineEdit(self.xmpTab)
        self.interviewerLine.setObjectName("interviewerLine")
        self.horizontalLayout_13.addWidget(self.interviewerLine)
        self.verticalLayout_2.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.creationDateLabel_5 = QtWidgets.QLabel(self.xmpTab)
        self.creationDateLabel_5.setObjectName("creationDateLabel_5")
        self.horizontalLayout_14.addWidget(self.creationDateLabel_5)
        self.intervieweeLine = QtWidgets.QLineEdit(self.xmpTab)
        self.intervieweeLine.setObjectName("intervieweeLine")
        self.horizontalLayout_14.addWidget(self.intervieweeLine)
        self.verticalLayout_2.addLayout(self.horizontalLayout_14)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_10.addLayout(self.verticalLayout_2)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.formLayout_15 = QtWidgets.QFormLayout()
        self.formLayout_15.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_15.setObjectName("formLayout_15")
        self.commentLabel_2 = QtWidgets.QLabel(self.xmpTab)
        self.commentLabel_2.setObjectName("commentLabel_2")
        self.formLayout_15.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.commentLabel_2)
        self.descriptionText = QtWidgets.QPlainTextEdit(self.xmpTab)
        self.descriptionText.setObjectName("descriptionText")
        self.formLayout_15.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.descriptionText)
        self.horizontalLayout_12.addLayout(self.formLayout_15)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_12)
        self.gridLayout_7.addLayout(self.horizontalLayout_10, 0, 0, 1, 1)
        self.tabWidget.addTab(self.xmpTab, "")
        self.gridLayout_8.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.label_2 = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setPointSize(32)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.label = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(self.page_2)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.gridLayout_9.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.gridLayout_4.addWidget(self.stackedWidget, 0, 0, 1, 1)
        autoBWF.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(autoBWF)
        self.statusbar.setObjectName("statusbar")
        autoBWF.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(autoBWF)
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        autoBWF.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionUpdate_metadata = QtWidgets.QAction(autoBWF)
        self.actionUpdate_metadata.setCheckable(False)
        self.actionUpdate_metadata.setObjectName("actionUpdate_metadata")
        self.actionOpen = QtWidgets.QAction(autoBWF)
        self.actionOpen.setObjectName("actionOpen")
        self.actionQuit = QtWidgets.QAction(autoBWF)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpen_template = QtWidgets.QAction(autoBWF)
        self.actionOpen_template.setEnabled(True)
        self.actionOpen_template.setObjectName("actionOpen_template")
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionOpen_template)
        self.toolBar.addAction(self.actionUpdate_metadata)
        self.toolBar.addAction(self.actionQuit)

        self.retranslateUi(autoBWF)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(autoBWF)

    def retranslateUi(self, autoBWF):
        _translate = QtCore.QCoreApplication.translate
        autoBWF.setWindowTitle(_translate("autoBWF", "autoBWF"))
        self.descriptionLabel.setText(_translate("autoBWF", "Description"))
        self.originatorLabel.setText(_translate("autoBWF", "Originator"))
        self.originatorRefLabel.setText(_translate("autoBWF", "OriginatorRef"))
        self.originationDateLabel.setText(_translate("autoBWF", "OriginationDate"))
        self.originationTimeLabel.setText(_translate("autoBWF", "OriginationTime"))
        self.md5Check.setText(_translate("autoBWF", "Embed MD5 of data chunk"))
        self.codingHistoryLabel.setText(_translate("autoBWF", "CodingHistory"))
        self.label_7.setText(_translate("autoBWF", "Speed"))
        self.label_13.setText(_translate("autoBWF", "Tape type"))
        self.label_12.setText(_translate("autoBWF", "EQ"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bwfTab), _translate("autoBWF", "BWF"))
        self.titleLabel.setText(_translate("autoBWF", "Title (INAM)"))
        self.creationDateLabel.setText(_translate("autoBWF", "Creation Date (ICRD)"))
        self.commentLabel.setText(_translate("autoBWF", "Comment (ICMT)"))
        self.sourceLabel.setText(_translate("autoBWF", "Source (ISRC)"))
        self.technicianLabel.setText(_translate("autoBWF", "Technician (ITCH)"))
        self.isftLabel.setText(_translate("autoBWF", "ISFT"))
        self.copyrightLabel.setText(_translate("autoBWF", "Copyright (ICOP)"))
        self.label_10.setText(_translate("autoBWF", "Replace with boilerplate:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.riffTab), _translate("autoBWF", "RIFF"))
        self.creationDateLabel_2.setText(_translate("autoBWF", "Language"))
        self.sourceLabel_2.setText(_translate("autoBWF", "Copyright holder"))
        self.creationDateLabel_4.setText(_translate("autoBWF", "Interviewer"))
        self.creationDateLabel_5.setText(_translate("autoBWF", "Interviewee"))
        self.commentLabel_2.setText(_translate("autoBWF", "Description"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.xmpTab), _translate("autoBWF", "XMP"))
        self.label_2.setText(_translate("autoBWF", "Saving metadata. Please wait..."))
        self.label.setText(_translate("autoBWF", "TextLabel"))
        self.toolBar.setWindowTitle(_translate("autoBWF", "toolBar"))
        self.actionUpdate_metadata.setText(_translate("autoBWF", "Save metadata"))
        self.actionUpdate_metadata.setShortcut(_translate("autoBWF", "S"))
        self.actionOpen.setText(_translate("autoBWF", "Open"))
        self.actionOpen.setShortcut(_translate("autoBWF", "O"))
        self.actionQuit.setText(_translate("autoBWF", "Quit"))
        self.actionQuit.setShortcut(_translate("autoBWF", "Q"))
        self.actionOpen_template.setText(_translate("autoBWF", "Load template..."))
        self.actionOpen_template.setToolTip(_translate("autoBWF", "Load template"))
        self.actionOpen_template.setShortcut(_translate("autoBWF", "T"))


