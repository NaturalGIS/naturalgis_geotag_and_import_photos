# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/settingsdialogbase.ui'
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
        Dialog.resize(400, 169)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.leExifToolPath = QtGui.QLineEdit(Dialog)
        self.leExifToolPath.setObjectName(_fromUtf8("leExifToolPath"))
        self.horizontalLayout.addWidget(self.leExifToolPath)
        self.btnSelectBinary = QtGui.QPushButton(Dialog)
        self.btnSelectBinary.setObjectName(_fromUtf8("btnSelectBinary"))
        self.horizontalLayout.addWidget(self.btnSelectBinary)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.leConfigPath = QtGui.QLineEdit(Dialog)
        self.leConfigPath.setObjectName(_fromUtf8("leConfigPath"))
        self.horizontalLayout_2.addWidget(self.leConfigPath)
        self.btnSelectConfig = QtGui.QPushButton(Dialog)
        self.btnSelectConfig.setObjectName(_fromUtf8("btnSelectConfig"))
        self.horizontalLayout_2.addWidget(self.btnSelectConfig)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Path to ExifTool executable", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectBinary.setText(QtGui.QApplication.translate("Dialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Path to ExifTool config file", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectConfig.setText(QtGui.QApplication.translate("Dialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))

