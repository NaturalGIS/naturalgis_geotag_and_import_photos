# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/directoryselectorbase.ui'
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

class Ui_DirectorySelector(object):
    def setupUi(self, DirectorySelector):
        DirectorySelector.setObjectName(_fromUtf8("DirectorySelector"))
        DirectorySelector.resize(329, 27)
        self.horizontalLayout = QtGui.QHBoxLayout(DirectorySelector)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit = QtGui.QLineEdit(DirectorySelector)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.btnSelect = QtGui.QToolButton(DirectorySelector)
        self.btnSelect.setObjectName(_fromUtf8("btnSelect"))
        self.horizontalLayout.addWidget(self.btnSelect)

        self.retranslateUi(DirectorySelector)
        QtCore.QMetaObject.connectSlotsByName(DirectorySelector)

    def retranslateUi(self, DirectorySelector):
        DirectorySelector.setWindowTitle(QtGui.QApplication.translate("DirectorySelector", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelect.setText(QtGui.QApplication.translate("DirectorySelector", "...", None, QtGui.QApplication.UnicodeUTF8))

