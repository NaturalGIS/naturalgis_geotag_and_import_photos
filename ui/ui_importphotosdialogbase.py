# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/importphotosdialogbase.ui'
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
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lePhotosPath = QtGui.QLineEdit(Dialog)
        self.lePhotosPath.setObjectName(_fromUtf8("lePhotosPath"))
        self.horizontalLayout.addWidget(self.lePhotosPath)
        self.btnSelectPhotos = QtGui.QPushButton(Dialog)
        self.btnSelectPhotos.setObjectName(_fromUtf8("btnSelectPhotos"))
        self.horizontalLayout.addWidget(self.btnSelectPhotos)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.chkRecurse = QtGui.QCheckBox(Dialog)
        self.chkRecurse.setObjectName(_fromUtf8("chkRecurse"))
        self.verticalLayout.addWidget(self.chkRecurse)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.leShapePath = QtGui.QLineEdit(Dialog)
        self.leShapePath.setObjectName(_fromUtf8("leShapePath"))
        self.horizontalLayout_2.addWidget(self.leShapePath)
        self.btnSelectShape = QtGui.QPushButton(Dialog)
        self.btnSelectShape.setObjectName(_fromUtf8("btnSelectShape"))
        self.horizontalLayout_2.addWidget(self.btnSelectShape)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.chkAppend = QtGui.QCheckBox(Dialog)
        self.chkAppend.setEnabled(True)
        self.chkAppend.setObjectName(_fromUtf8("chkAppend"))
        self.verticalLayout.addWidget(self.chkAppend)
        self.chkAddToCanvas = QtGui.QCheckBox(Dialog)
        self.chkAddToCanvas.setObjectName(_fromUtf8("chkAddToCanvas"))
        self.verticalLayout.addWidget(self.chkAddToCanvas)
        self.lstTags = QtGui.QTreeWidget(Dialog)
        self.lstTags.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.lstTags.setAlternatingRowColors(True)
        self.lstTags.setRootIsDecorated(False)
        self.lstTags.setObjectName(_fromUtf8("lstTags"))
        self.verticalLayout.addWidget(self.lstTags)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.btnSelectAll = QtGui.QPushButton(Dialog)
        self.btnSelectAll.setObjectName(_fromUtf8("btnSelectAll"))
        self.horizontalLayout_3.addWidget(self.btnSelectAll)
        self.btnClearAll = QtGui.QPushButton(Dialog)
        self.btnClearAll.setObjectName(_fromUtf8("btnClearAll"))
        self.horizontalLayout_3.addWidget(self.btnClearAll)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.leConfigFile = QtGui.QLineEdit(Dialog)
        self.leConfigFile.setObjectName(_fromUtf8("leConfigFile"))
        self.horizontalLayout_4.addWidget(self.leConfigFile)
        self.btnSelectConfig = QtGui.QPushButton(Dialog)
        self.btnSelectConfig.setObjectName(_fromUtf8("btnSelectConfig"))
        self.horizontalLayout_4.addWidget(self.btnSelectConfig)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Import photos", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Path to photos", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectPhotos.setText(QtGui.QApplication.translate("Dialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.chkRecurse.setText(QtGui.QApplication.translate("Dialog", "Recurse subdirectories", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Output shapefile", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectShape.setText(QtGui.QApplication.translate("Dialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.chkAppend.setText(QtGui.QApplication.translate("Dialog", "Append to existing file", None, QtGui.QApplication.UnicodeUTF8))
        self.chkAddToCanvas.setText(QtGui.QApplication.translate("Dialog", "Add result to canvas", None, QtGui.QApplication.UnicodeUTF8))
        self.lstTags.setSortingEnabled(False)
        self.lstTags.headerItem().setText(0, QtGui.QApplication.translate("Dialog", "EXIF tags", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectAll.setText(QtGui.QApplication.translate("Dialog", "Select all", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClearAll.setText(QtGui.QApplication.translate("Dialog", "Clear selection", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "ExifTool config", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectConfig.setText(QtGui.QApplication.translate("Dialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))

