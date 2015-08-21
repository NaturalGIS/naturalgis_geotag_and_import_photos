# -*- coding: utf-8 -*-

#******************************************************************************
#
# Geotag and import photos
# ---------------------------------------------------------
# Process photos from phototraps.
#
# Copyright (C) 2012-2013 Alexander Bruy (alexander.bruy@gmail.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************


import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

import directorydelegate
import uniquevaluesdelegate
import tagphotosthread
import geotagphotos_utils as utils

from ui.ui_tagphotosdialogbase import Ui_Dialog


class TagPhotosDialog(QDialog, Ui_Dialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.workThread = None

        self.btnOk = self.buttonBox.button(QDialogButtonBox.Ok)
        self.btnClose = self.buttonBox.button(QDialogButtonBox.Close)

        self.model = QStandardItemModel(0, 3)
        self.model.rowsInserted.connect(self.toggleButtons)
        self.model.rowsRemoved.connect(self.toggleButtons)

        self.cmbLayers.currentIndexChanged.connect(self.reloadFields)
        self.cmbTags.currentIndexChanged.connect(self.resetTagsEditor)
        self.cmbValues.currentIndexChanged.connect(self.resetValuesEditor)

        self.btnAddRow.clicked.connect(self.addRow)
        self.btnDeleteRow.clicked.connect(self.deleteRow)
        self.btnClearAll.clicked.connect(self.clearAll)

        self.btnSelectConfig.clicked.connect(self.selectConfigFile)

        self.manageGui()

    def manageGui(self):
        self.btnDeleteRow.setEnabled(False)
        self.btnClearAll.setEnabled(False)

        self.setTableHeader()
        self.tableView.setModel(self.model)
        self.dirDelegate = directorydelegate.DirectoryDelegate()
        self.tableView.setItemDelegateForColumn(0, self.dirDelegate)

        self.cmbLayers.clear()
        self.cmbLayers.addItems(utils.getVectorLayerNames())

    def setTableHeader(self):
        self.model.setHorizontalHeaderLabels([self.tr("Path to folder"),
                                              self.tr("Tag name"),
                                              self.tr("Tag value")
                                            ])

    def reloadFields(self):
        self.cmbTags.clear()
        self.cmbValues.clear()
        layer = utils.getVectorLayerByName(self.cmbLayers.currentText())
        fields = utils.getFieldNames(layer)

        self.cmbTags.addItems(fields)
        self.cmbValues.addItems(fields)

        self.resetTagsEditor()
        self.resetValuesEditor()

    def resetTagsEditor(self):
        myLayer = utils.getVectorLayerByName(self.cmbLayers.currentText())

        self.tagDelegate = uniquevaluesdelegate.UniqueValuesDelegate(layer=myLayer, field=self.cmbTags.currentText())
        self.tableView.setItemDelegateForColumn(1, self.tagDelegate)

    def resetValuesEditor(self):
        myLayer = utils.getVectorLayerByName(self.cmbLayers.currentText())

        self.valuesDelegate = uniquevaluesdelegate.UniqueValuesDelegate(layer=myLayer, field=self.cmbValues.currentText())
        self.tableView.setItemDelegateForColumn(2, self.valuesDelegate)

    def addRow(self):
        self.model.appendRow([QStandardItem(""),
                              QStandardItem(""),
                              QStandardItem("")
                            ])

    def deleteRow(self):
        indexes = self.tableView.selectionModel().selectedIndexes()
        if len(indexes) > 0:
            self.model.removeRows(indexes[0].row(), 1)

    def clearAll(self):
        self.model.clear()
        self.setTableHeader()
        self.toggleButtons()

    def selectConfigFile(self):
        settings = QSettings("Faunalia", "Geotagphotos")
        lastDir = settings.value("ui/lastConfigDir", "")
        fileName = QFileDialog.getOpenFileName(None,
                                               self.tr("Select config file"),
                                               lastDir,
                                               self.tr("All files (*)")
                                              )
        if fileName == "":
            return

        self.leConfigFile.setText(fileName)
        settings.setValue("ui/lastConfigDir", os.path.dirname(unicode(fileName)))

    def toggleButtons(self):
        rows = self.model.rowCount()
        if rows == 0:
            self.btnDeleteRow.setEnabled(False)
            self.btnClearAll.setEnabled(False)
        else:
            self.btnDeleteRow.setEnabled(True)
            self.btnClearAll.setEnabled(True)

    def accept(self):
        # check if all necessary data entered
        rows = self.model.rowCount()
        if rows == 0:
            QMessageBox.warning(self,
                                 self.tr("No data found"),
                                 self.tr("Seems there are no data loaded. Please populate table first."))
            return

        noTags = True
        for r in xrange(rows):
            item = self.model.item(r, 1)
            if item and item.text() != "":
                noTags = False
                break

        if noTags:
            QMessageBox.warning(self,
                                self.tr("No tags specified"),
                                self.tr("Please specify tags to add/modify."))
            return

        if self.workThread is not None:
            QMessageBox.warning(self,
                                self.tr("Active process found"),
                                self.tr("Running process found. Please wait until it finished."))
            return

        # config file
        cfgFile = self.leConfigFile.text()
        if cfgFile == "":
            cfgFile = utils.getConfigPath()

        # tagging
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.btnOk.setEnabled(False)

        self.workThread = tagphotosthread.TagPhotosThread(self.model, cfgFile)

        self.workThread.rangeChanged.connect(self.setProgressRange)
        self.workThread.updateProgress.connect(self.updateProgress)
        self.workThread.processFinished.connect(self.processFinished)
        self.workThread.processInterrupted.connect(self.processInterrupted)

        self.btnClose.setText(self.tr("Cancel"))
        self.buttonBox.rejected.disconnect(self.reject)
        self.btnClose.clicked.connect(self.stopProcessing)

        self.workThread.start()

    def reject(self):
        QDialog.reject(self)

    def stopProcessing(self):
        if self.workThread is not None:
            self.workThread.stop()
            self.workThread = None

    def setProgressRange(self, data):
        if data[0] != "":
            self.progressBar.setFormat(data[0])

        self.progressBar.setRange(0, data[1])

    def updateProgress(self):
        self.progressBar.setValue(self.progressBar.value() + 1)

    def processFinished(self):
        self.stopProcessing()
        self.restoreGui()

        QMessageBox.information(self,
                                self.tr("Geotag and import photos"),
                                self.tr("Tagging completed!"))

    def processInterrupted(self):
        self.restoreGui()

    def restoreGui(self):
        self.progressBar.setFormat("%p%")
        self.progressBar.setRange(0, 1)
        self.progressBar.setValue(0)

        self.buttonBox.rejected.connect(self.reject)
        self.btnClose.clicked.disconnect(self.stopProcessing)
        self.btnClose.setText(self.tr("Close"))
        self.btnOk.setEnabled(True)

        QApplication.restoreOverrideCursor()
