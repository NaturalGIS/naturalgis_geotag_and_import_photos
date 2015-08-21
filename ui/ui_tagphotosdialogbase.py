# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/tagphotosdialogbase.ui'
#
# Created: Mon Jul 29 20:12:08 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(464, 467)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.cmbLayers = QtGui.QComboBox(Dialog)
        self.cmbLayers.setObjectName(_fromUtf8("cmbLayers"))
        self.gridLayout.addWidget(self.cmbLayers, 0, 1, 1, 2)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cmbTags = QtGui.QComboBox(Dialog)
        self.cmbTags.setObjectName(_fromUtf8("cmbTags"))
        self.gridLayout.addWidget(self.cmbTags, 1, 1, 1, 2)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.cmbValues = QtGui.QComboBox(Dialog)
        self.cmbValues.setObjectName(_fromUtf8("cmbValues"))
        self.gridLayout.addWidget(self.cmbValues, 2, 1, 1, 2)
        self.tableView = QtGui.QTableView(Dialog)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setWordWrap(False)
        self.tableView.setCornerButtonEnabled(False)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableView, 3, 0, 1, 3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnAddRow = QtGui.QPushButton(Dialog)
        self.btnAddRow.setObjectName(_fromUtf8("btnAddRow"))
        self.horizontalLayout.addWidget(self.btnAddRow)
        self.btnDeleteRow = QtGui.QPushButton(Dialog)
        self.btnDeleteRow.setObjectName(_fromUtf8("btnDeleteRow"))
        self.horizontalLayout.addWidget(self.btnDeleteRow)
        self.btnClearAll = QtGui.QPushButton(Dialog)
        self.btnClearAll.setObjectName(_fromUtf8("btnClearAll"))
        self.horizontalLayout.addWidget(self.btnClearAll)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.leConfigFile = QtGui.QLineEdit(Dialog)
        self.leConfigFile.setObjectName(_fromUtf8("leConfigFile"))
        self.horizontalLayout_2.addWidget(self.leConfigFile)
        self.btnSelectConfig = QtGui.QPushButton(Dialog)
        self.btnSelectConfig.setObjectName(_fromUtf8("btnSelectConfig"))
        self.horizontalLayout_2.addWidget(self.btnSelectConfig)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 0, 1, 3)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 6, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Tag photos", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Vector layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Tag names", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Tag values", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAddRow.setText(QtGui.QApplication.translate("Dialog", "Add row", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDeleteRow.setText(QtGui.QApplication.translate("Dialog", "Delete row", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClearAll.setText(QtGui.QApplication.translate("Dialog", "Clear all", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "ExifTool config", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectConfig.setText(QtGui.QApplication.translate("Dialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))

