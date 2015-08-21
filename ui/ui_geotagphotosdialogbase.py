# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/geotagphotosdialogbase.ui'
#
# Created: Mon Jul 29 20:12:07 2013
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
        Dialog.resize(467, 468)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.cmbLayers = QtGui.QComboBox(Dialog)
        self.cmbLayers.setObjectName(_fromUtf8("cmbLayers"))
        self.gridLayout.addWidget(self.cmbLayers, 0, 1, 1, 3)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cmbFields = QtGui.QComboBox(Dialog)
        self.cmbFields.setObjectName(_fromUtf8("cmbFields"))
        self.gridLayout.addWidget(self.cmbFields, 1, 1, 1, 3)
        self.tableView = QtGui.QTableView(Dialog)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setWordWrap(False)
        self.tableView.setCornerButtonEnabled(False)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableView, 2, 0, 1, 4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnPopulate = QtGui.QPushButton(Dialog)
        self.btnPopulate.setObjectName(_fromUtf8("btnPopulate"))
        self.horizontalLayout.addWidget(self.btnPopulate)
        self.btnAddRow = QtGui.QPushButton(Dialog)
        self.btnAddRow.setObjectName(_fromUtf8("btnAddRow"))
        self.horizontalLayout.addWidget(self.btnAddRow)
        self.btnDeleteRow = QtGui.QPushButton(Dialog)
        self.btnDeleteRow.setObjectName(_fromUtf8("btnDeleteRow"))
        self.horizontalLayout.addWidget(self.btnDeleteRow)
        self.btnClearAll = QtGui.QPushButton(Dialog)
        self.btnClearAll.setObjectName(_fromUtf8("btnClearAll"))
        self.horizontalLayout.addWidget(self.btnClearAll)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 4)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.chkLongitudeAsE = QtGui.QCheckBox(self.groupBox)
        self.chkLongitudeAsE.setObjectName(_fromUtf8("chkLongitudeAsE"))
        self.verticalLayout.addWidget(self.chkLongitudeAsE)
        self.chkLatitudeAsS = QtGui.QCheckBox(self.groupBox)
        self.chkLatitudeAsS.setObjectName(_fromUtf8("chkLatitudeAsS"))
        self.verticalLayout.addWidget(self.chkLatitudeAsS)
        self.chkRenameFiles = QtGui.QCheckBox(self.groupBox)
        self.chkRenameFiles.setObjectName(_fromUtf8("chkRenameFiles"))
        self.verticalLayout.addWidget(self.chkRenameFiles)
        self.gridLayout.addWidget(self.groupBox, 4, 0, 1, 4)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 5, 0, 1, 4)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 2, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Geotag photos", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Vector layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Label field", None, QtGui.QApplication.UnicodeUTF8))
        self.btnPopulate.setText(QtGui.QApplication.translate("Dialog", "Populate table from layer", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAddRow.setText(QtGui.QApplication.translate("Dialog", "Add row", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDeleteRow.setText(QtGui.QApplication.translate("Dialog", "Delete row", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClearAll.setText(QtGui.QApplication.translate("Dialog", "Clear all", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Geotagging options", None, QtGui.QApplication.UnicodeUTF8))
        self.chkLongitudeAsE.setText(QtGui.QApplication.translate("Dialog", "Longitude E (by default W)", None, QtGui.QApplication.UnicodeUTF8))
        self.chkLatitudeAsS.setText(QtGui.QApplication.translate("Dialog", "Latitude S (by default N)", None, QtGui.QApplication.UnicodeUTF8))
        self.chkRenameFiles.setText(QtGui.QApplication.translate("Dialog", "Rename geotagged files", None, QtGui.QApplication.UnicodeUTF8))

