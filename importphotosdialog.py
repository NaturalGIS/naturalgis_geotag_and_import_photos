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

import importthread
import geotagphotos_utils as utils

import exiftool

from ui.ui_importphotosdialogbase import Ui_Dialog


class ImportPhotosDialog(QDialog, Ui_Dialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.workThread = None
        self.outFileName = None
        self.outEncoding = None

        self.btnOk = self.buttonBox.button(QDialogButtonBox.Ok)
        self.btnClose = self.buttonBox.button(QDialogButtonBox.Close)

        self.btnSelectPhotos.clicked.connect(self.selectPhotosDir)
        self.btnSelectShape.clicked.connect(self.selectOutputShape)

        self.btnSelectAll.clicked.connect(self.selectAllTags)
        self.btnClearAll.clicked.connect(self.clearAllTags)

        self.btnSelectConfig.clicked.connect(self.selectConfigFile)

        self.manageGui()

    def manageGui(self):
        # read settings and restore controls state
        settings = QSettings("Faunalia", "Geotagphotos")
        self.chkRecurse.setChecked(bool(settings.value("ui/recurseDirs", False)))
        self.chkAppend.setChecked(bool(settings.value("ui/appendFile", False)))
        self.chkAddToCanvas.setChecked(bool(settings.value("ui/addToCanvas", False)))

    def selectPhotosDir(self):
        settings = QSettings("Faunalia", "Geotagphotos")
        lastDir = settings.value("ui/lastPhotosDir", "")
        dirName = QFileDialog.getExistingDirectory(None,
                                                   self.tr("Select directory"),
                                                   lastDir,
                                                   QFileDialog.ShowDirsOnly)
        if dirName == "":
            return

        self.lePhotosPath.setText(dirName)
        settings.setValue("ui/lastPhotosDir", os.path.dirname(unicode(dirName)))

        self.loadTags(dirName)

    def selectOutputShape(self):
        (self.outFileName, self.outEncoding) = utils.saveDialog(self)
        if self.outFileName is None or self.outEncoding is None:
            return

        self.leShapePath.setText(self.outFileName)

    def loadTags(self, dirName):
        if dirName == "":
            return

        self.lstTags.clear()

        etPath = utils.getExifToolPath()
        if not etPath == "":
            etPath = os.path.join(os.path.normpath(unicode(etPath)), "exiftool")
        else:
            etPath = "exiftool"

        # config file
        cfgFile = self.leConfigFile.text()
        if cfgFile == "":
            cfgFile = utils.getConfigPath()

        if cfgFile != "":
            etPath += " -config " + unicode(cfgFile)

        et = exiftool.ExifTool(etPath)

        md = None
        found = False

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        # fetch metadata from first photo
        with et:
            for root, dirs, files in os.walk(unicode(dirName)):
                if len(files) == 0:
                    continue

                for f in files:
                    if f.lower().endswith(".jpg") or f.lower().endswith(".jpeg"):
                        md = et.get_metadata(os.path.join(root, f))
                        if len(md) > 0:
                            found = True
                            break

                if found:
                    break

        # process metadata and populate tag list
        for k, v in md.iteritems():
            if not k.startswith("EXIF:"):
                continue
            ti = QTreeWidgetItem(self.lstTags)
            ti.setText(0, k)
            ti.setCheckState(0, Qt.Unchecked)
        self.lstTags.sortItems(0, Qt.AscendingOrder)

        QApplication.restoreOverrideCursor()

    def selectAllTags(self):
        for i in xrange(self.lstTags.topLevelItemCount()):
            self.lstTags.topLevelItem(i).setCheckState(0, Qt.Checked)

    def clearAllTags(self):
        for i in xrange(self.lstTags.topLevelItemCount()):
            self.lstTags.topLevelItem(i).setCheckState(0, Qt.Unchecked)

    def selectConfigFile(self):
        settings = QSettings("Faunalia", "Geotagphotos")
        lastDir = settings.value("ui/lastConfigDir", "")
        fileName = QFileDialog.getOpenFileName(None,
                                               self.tr("Select config file"),
                                               lastDir,
                                               self.tr("All files (*)"))
        if fileName == "":
            return

        self.leConfigFile.setText(fileName)
        settings.setValue("ui/lastConfigDir", os.path.dirname(unicode(fileName)))

        # reread tags
        self.loadTags(self.lePhotosPath.text())

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        # check if exiftool installed
        if not utils.exiftoolInstalled():
            QMessageBox.warning(self,
                                self.tr("Missing exiftool"),
                                self.tr("Can't locate exiftool executable! Make sure that it is installed and available in PATH or, alternatively, specify path to binary in plugin settings"))
            return

        # save ui state
        settings = QSettings("Faunalia", "Geotagphotos")
        settings.setValue("ui/recurseDirs", self.chkRecurse.isChecked())
        settings.setValue("ui/appendFile", self.chkAppend.isChecked())
        settings.setValue("ui/addToCanvas", self.chkAddToCanvas.isChecked())

        if self.lePhotosPath.text() == "":
            QMessageBox.warning(self,
                                self.tr("Path not set"),
                                self.tr("Path to photos is not set. Please specify directory with photos."))
            return

        if self.outFileName is None or self.outFileName == "":
            QMessageBox.warning(self,
                                self.tr("Output file is not set"),
                                self.tr("Output file name is missing. Please specify correct output file."))
            return

        # TODO: check for fields compatibility?

        # config file
        cfgFile = self.leConfigFile.text()
        if cfgFile == "":
            cfgFile = utils.getConfigPath()

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.btnOk.setEnabled(False)

        tagList = []
        for i in xrange(self.lstTags.topLevelItemCount()):
            item = self.lstTags.topLevelItem(i)
            if item.checkState(0) == Qt.Checked:
                tagList.append(unicode(item.text(0)))

        self.workThread = importthread.ImportThread(self.lePhotosPath.text(),
                                                    self.chkRecurse.isChecked(),
                                                    tagList,
                                                    self.outFileName,
                                                    self.outEncoding,
                                                    self.chkAppend.isChecked(),
                                                    cfgFile)

        self.workThread.rangeChanged.connect(self.setProgressRange)
        self.workThread.updateProgress.connect(self.updateProgress)
        self.workThread.processFinished.connect(self.processFinished)
        self.workThread.processInterrupted.connect(self.processInterrupted)

        self.btnClose.setText(self.tr("Cancel"))
        self.buttonBox.rejected.disconnect(self.reject)
        self.btnClose.clicked.connect(self.stopProcessing)

        self.workThread.start()

    def setProgressRange(self, data):
        if data[0] != "":
            self.progressBar.setFormat(data[0])

        self.progressBar.setRange(0, data[1])

    def updateProgress(self):
        self.progressBar.setValue(self.progressBar.value() + 1)

    def processFinished(self, hasOutput):
        self.stopProcessing()
        self.restoreGui()

        if not hasOutput:
            QMessageBox.warning(self,
                                self.tr("No output file"),
                                self.tr("There are no geotagged photos in selected directory.\nShapefile was not created/updated."))

        if self.chkAddToCanvas.isChecked():
            if self.chkAppend.isChecked() or hasOutput:
                self.addLayerToCanvas()

    def processInterrupted(self):
        self.restoreGui()

    def stopProcessing(self):
        if self.workThread is not None:
            self.workThread.stop()
            self.workThread = None

    def restoreGui(self):
        self.progressBar.setFormat("%p%")
        self.progressBar.setRange(0, 1)
        self.progressBar.setValue(0)

        self.buttonBox.rejected.connect(self.reject)
        self.btnClose.clicked.disconnect(self.stopProcessing)
        self.btnClose.setText(self.tr("Close"))
        self.btnOk.setEnabled(True)
        QApplication.restoreOverrideCursor()

    def addLayerToCanvas(self):
        newLayer = QgsVectorLayer(self.outFileName, QFileInfo(self.outFileName).baseName(), "ogr")

        if newLayer.isValid():
            QgsMapLayerRegistry.instance().addMapLayer(newLayer)
        else:
            QMessageBox.warning(self,
                                self.tr("Can't open file"),
                                self.tr("Error loading output shapefile:\n%s") % unicode(self.outFileName))
