# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/uniquevaluesselectorbase.ui'
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

class Ui_UniqueValuesSelector(object):
    def setupUi(self, UniqueValuesSelector):
        UniqueValuesSelector.setObjectName(_fromUtf8("UniqueValuesSelector"))
        UniqueValuesSelector.resize(400, 24)
        self.verticalLayout = QtGui.QVBoxLayout(UniqueValuesSelector)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.comboBox = QtGui.QComboBox(UniqueValuesSelector)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.verticalLayout.addWidget(self.comboBox)

        self.retranslateUi(UniqueValuesSelector)
        QtCore.QMetaObject.connectSlotsByName(UniqueValuesSelector)

    def retranslateUi(self, UniqueValuesSelector):
        UniqueValuesSelector.setWindowTitle(QtGui.QApplication.translate("UniqueValuesSelector", "Form", None, QtGui.QApplication.UnicodeUTF8))

