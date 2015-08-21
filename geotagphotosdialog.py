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


from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

import layerreaderthread
import geotaggingthread
import directorydelegate
import geotagphotos_utils as utils

from ui.ui_geotagphotosdialogbase import Ui_Dialog


class GeotagPhotosDialog(QDialog, Ui_Dialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.workThread = None

        self.btnOk = self.buttonBox.button(QDialogButtonBox.Ok)
        self.btnClose = self.buttonBox.button(QDialogButtonBox.Close)

        self.model = QStandardItemModel(0, 4)
        self.model.rowsInserted.connect(self.toggleButtons)
        self.model.rowsRemoved.connect(self.toggleButtons)

        self.cmbLayers.currentIndexChanged.connect(self.reloadFields)

        self.btnAddRow.clicked.connect(self.addRow)
        self.btnDeleteRow.clicked.connect(self.deleteRow)
        self.btnClearAll.clicked.connect(self.clearAll)

        self.btnPopulate.clicked.connect(self.populateTable)

        self.manageGui()

    def manageGui(self):
        self.btnDeleteRow.setEnabled(False)
        self.btnClearAll.setEnabled(False)

        self.setTableHeader()
        self.tableView.setModel(self.model)
        self.delegate = directorydelegate.DirectoryDelegate()
        self.tableView.setItemDelegateForColumn(3, self.delegate)

        self.cmbLayers.clear()
        self.cmbLayers.addItems(utils.getVectorLayerNames())

        # read settings and restore controls state
        settings = QSettings("Faunalia", "Geotagphotos")
        self.chkLongitudeAsE.setChecked(bool(settings.value("ui/longitude", False)))
        self.chkLatitudeAsS.setChecked(bool(settings.value("ui/latitude", False)))
        self.chkRenameFiles.setChecked(bool(settings.value("ui/renameFiles", False)))

    def setTableHeader(self):
        self.model.setHorizontalHeaderLabels([self.tr("Label"),
                                              self.tr("X"),
                                              self.tr("Y"),
                                              self.tr("Path to folder")
                                            ])

    def reloadFields(self):
        self.cmbFields.clear()
        layer = utils.getVectorLayerByName(self.cmbLayers.currentText())
        self.cmbFields.addItems(utils.getFieldNames(layer))

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

    def toggleButtons(self):
        rows = self.model.rowCount()
        if rows == 0:
            self.btnDeleteRow.setEnabled(False)
            self.btnClearAll.setEnabled(False)
        else:
            self.btnDeleteRow.setEnabled(True)
            self.btnClearAll.setEnabled(True)

    def populateTable(self):
        layer = utils.getVectorLayerByName(self.cmbLayers.currentText())

        if not layer.crs().geographicFlag():
            QMessageBox.warning(self,
                                self.tr("Wrong layer CRS"),
                                self.tr("Selected layer has projected CRS. Please choose layer with geographic CRS or reproject this one.")
                               )
            return

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        self.model.clear()
        self.setTableHeader()

        self.workThread = layerreaderthread.LayerReaderThread(layer, self.cmbFields.currentText())
        self.workThread.rangeChanged.connect(self.setProgressRange)
        self.workThread.updateProgress.connect(self.updateProgressAndTable)
        self.workThread.processFinished.connect(self.populateFinished)
        self.workThread.processInterrupted.connect(self.populateInterrupted)

        self.btnPopulate.clicked.disconnect(self.populateTable)
        self.btnPopulate.clicked.connect(self.stopProcessing)
        self.btnPopulate.setText(self.tr("Cancel"))

        self.workThread.start()

    def accept(self):
        # check if exiftool installed
        if not utils.exiftoolInstalled():
            QMessageBox.warning(self,
                                self.tr("Missing exiftool"),
                                self.tr("Can't locate exiftool executable! Make sure that it is installed and available in PATH or, alternatively, specify path to binary in plugin settings"))
            return

        # save ui state
        settings = QSettings("Faunalia", "Geotagphotos")
        settings.setValue("ui/longitude", self.chkLongitudeAsE.isChecked())
        settings.setValue("ui/latitude", self.chkLatitudeAsS.isChecked())
        settings.setValue("ui/renameFiles", self.chkRenameFiles.isChecked())

        # check if all necessary data entered
        rows = self.model.rowCount()
        if rows == 0:
            QMessageBox.warning(self,
                                self.tr("No data found"),
                                self.tr("Seems there are no data loaded. Please populate table first."))
            return

       # TODO: check for coordinates?

        noFolders = True
        for r in xrange(rows):
            item = self.model.item(r, 3)
            if item and item.text() != "":
                noFolders = False
                break

        if noFolders:
            QMessageBox.warning(self,
                                self.tr("No folders specified"),
                                self.tr("Please associate at least one folder with point."))
            return

        if self.workThread is not None:
            QMessageBox.warning(self,
                                self.tr("Active process found"),
                                self.tr("Running process found. Please wait until it finished."))
            return

        lonRef = "W"
        latRef = "N"

        if self.chkLongitudeAsE.isChecked():
            lonRef = "E"

        if self.chkLatitudeAsS.isChecked():
            latRef = "S"

        # geotagging and renaming
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.btnOk.setEnabled(False)

        self.workThread = geotaggingthread.GeotaggingThread(self.model,
                                                            latRef,
                                                            lonRef,
                                                            self.chkRenameFiles.isChecked())

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

    def updateProgressAndTable(self, data):
        items = []
        for v in data:
            items.append(QStandardItem(unicode(v)))

        self.model.appendRow(items)
        self.progressBar.setValue(self.progressBar.value() + 1)

    def updateProgress(self):
        self.progressBar.setValue(self.progressBar.value() + 1)

    def populateFinished(self):
        self.stopProcessing()

        self.tableView.resizeRowsToContents()
        self.tableView.resizeColumnsToContents()

        self.btnPopulate.clicked.disconnect(self.stopProcessing)
        self.btnPopulate.clicked.connect(self.populateTable)
        self.btnPopulate.setText(self.tr("Populate table"))

        self.restoreGui(False)

    def populateInterrupted(self):
        self.restoreGui(False)

    def processFinished(self):
        self.stopProcessing()
        self.restoreGui(True)

        QMessageBox.information(self,
                                self.tr("Geotag and import photos"),
                                self.tr("Geotagging completed!"))

    def processInterrupted(self):
        self.restoreGui(True)

    def restoreGui(self, restoreSlots):
        self.progressBar.setFormat("%p%")
        self.progressBar.setRange(0, 1)
        self.progressBar.setValue(0)

        if restoreSlots:
            self.buttonBox.rejected.connect(self.reject)
            self.btnClose.clicked.disconnect(self.stopProcessing)
            self.btnClose.setText(self.tr("Close"))
            self.btnOk.setEnabled(True)

        QApplication.restoreOverrideCursor()
