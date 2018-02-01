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


import os.path

from PyQt4.QtCore import *

from qgis.core import *

import exiftool
import geotagphotos_utils as utils


class GeotaggingThread(QThread):
    rangeChanged = pyqtSignal(list)
    updateProgress = pyqtSignal()
    processFinished = pyqtSignal()
    processInterrupted = pyqtSignal()

    wildcards = [".jpg", ".jpeg", ".JPG", ".JPEG"]

    def __init__(self, model, latRef, lonRef, needRename):
        QThread.__init__(self, QThread.currentThread())
        self.mutex = QMutex()
        self.stopMe = 0
        self.interrupted = False

        self.model = model
        self.latRef = latRef
        self.lonRef = lonRef
        self.needRename = needRename

        self.command = "exiftool"
        self.arguments = []

    def run(self):
        self.runGeotagging()

        if not self.interrupted and self.needRename:
            self.runRename()

        if not self.interrupted:
            self.processFinished.emit()
        else:
            self.processInterrupted.emit()

    def runGeotagging(self):
        self.mutex.lock()
        self.stopMe = 0
        self.mutex.unlock()

        self.process = QProcess()
        utils.setProcessEnvironment(self.process)
        self.process.error.connect(self.geotagError)

        rows = self.model.rowCount()

        # get total folder count for progress indicator
        count = 0
        for r in xrange(rows):
            lat = self.model.item(r, 1).text()
            lon = self.model.item(r, 2).text()
            item = self.model.item(r, 3)
            if (item and item.text() == "") or (lat == "" or lon == ""):
                continue

            count += 1

        self.rangeChanged.emit([self.tr("Geotagging: %p%"), count])
        for r in xrange(rows):
            item = self.model.item(r, 3)
            if item is None:
                continue
            if item and item.text() == "":
                continue

            lon = self.model.item(r, 1).text()
            lat = self.model.item(r, 2).text()
            dirName = self.model.item(r, 3).text()

            self.arguments[:] = []
            self.arguments.append("-GPSLongitudeRef=%s" % self.lonRef)
            self.arguments.append("-GPSLongitude=%s" % lon)
            self.arguments.append("-GPSLatitudeRef=%s" % self.latRef)
            self.arguments.append("-GPSLatitude=%s" % lat)
            self.arguments.append("-ext")
            self.arguments.append("jpg")
            self.arguments.append("-r")
            self.arguments.append(dirName)

            self.process.start(self.command, self.arguments, QIODevice.ReadOnly)
            if not self.process.waitForFinished(-1):
                QgsMessageLog.logMessage(
                    "Failed to process directory " + dirName,
                    tag='Geotag and import photos',
                    level=QgsMessageLog.WARNING
                )

            self.updateProgress.emit()

            self.mutex.lock()
            s = self.stopMe
            self.mutex.unlock()
            if s == 1:
                self.interrupted = True
                break

    def runRename(self):
        etPath = utils.getExifToolPath()
        if etPath != "":
            etPath = os.path.join(os.path.normpath(unicode(etPath)), "exiftool")
        else:
            etPath = "exiftool"

        et = exiftool.ExifTool(etPath)

        filters = QDir.Files | QDir.NoSymLinks | QDir.NoDotAndDotDot
        nameFilter = ["*.jpg", "*.jpeg", "*.JPG", "*.JPEG"]

        rows = self.model.rowCount()

        with et:
            for r in xrange(rows):
                if self.interrupted:
                    break

                item = self.model.item(r, 3)
                if item is None:
                    continue
                if item and item.text() == "":
                    continue

                dirName = unicode(self.model.item(r, 3).text())
                areaName = os.path.basename(dirName)

                for root, dirs, files in os.walk(unicode(dirName)):
                    fileCount = len(QDir(root).entryList(nameFilter, filters))
                    if fileCount > 0:
                        trapName = os.path.split(root)[1]

                        if trapName == areaName:
                            areaName = ""

                        self.rangeChanged.emit([self.tr("Renaming: %p%"), fileCount])

                        dt = ""
                        num = 0
                        zcount = len(str(fileCount))

                        for f in files:
                            fullPath = os.path.join(root, f)
                            if os.path.isfile(fullPath) and (os.path.splitext(fullPath)[1] in self.wildcards):
                                dt = et.get_tag("EXIF:DateTimeOriginal", unicode(fullPath))

                                if areaName == "":
                                    newName ="%s_%s_%s.jpg" % (trapName, dt.replace(":", "-").replace(" ", "_"), str(num).zfill(zcount))
                                else:
                                    newName = "%s_%s_%s_%s.jpg" % (areaName, trapName, dt.replace(":", "-").replace(" ", "_"), str(num).zfill(zcount))
                                num += 1

                                try:
                                    os.rename(fullPath, os.path.join(root, unicode(newName)))
                                except OSError, e:
                                    QgsMessageLog.logMessage(
                                        e,
                                        tag='Geotag and import photos',
                                        level=QgsMessageLog.CRITICAL
                                    )

                                self.updateProgress.emit()

                                self.mutex.lock()
                                s = self.stopMe
                                self.mutex.unlock()
                                if s == 1:
                                    self.interrupted = True
                                    break

    def geotagError(self, error):
        QgsMessageLog.logMessage(
            error,
            tag='Geotag and import photos',
            level=QgsMessageLog.WARNING
        )

    def stop(self):
        self.mutex.lock()
        self.stopMe = 1
        self.mutex.unlock()

        QThread.wait(self)
