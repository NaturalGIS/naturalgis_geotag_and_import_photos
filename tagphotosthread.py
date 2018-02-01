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


class TagPhotosThread(QThread):
    rangeChanged = pyqtSignal(list)
    updateProgress = pyqtSignal()
    processFinished = pyqtSignal()
    processInterrupted = pyqtSignal()

    wildcards = [".jpg", ".jpeg", ".JPG", ".JPEG"]

    def __init__(self, model, config):
        QThread.__init__(self, QThread.currentThread())
        self.mutex = QMutex()
        self.stopMe = 0
        self.interrupted = False

        self.model = model
        self.configFile = config

        self.command = "exiftool"
        self.arguments = []

    def run(self):
        self.mutex.lock()
        self.stopMe = 0
        self.mutex.unlock()

        self.process = QProcess()
        utils.setProcessEnvironment(self.process)
        self.process.error.connect(self.taggingError)

        rows = self.model.rowCount()

        # get total folder count for progress indicator
        count = 0
        for r in xrange(rows):
            tag = self.model.item(r, 0).text()
            val = self.model.item(r, 1).text()
            item = self.model.item(r, 2)
            if (item and item.text() == "") or (tag == "" or val == ""):
                continue

            count += 1

        self.rangeChanged.emit([self.tr("Tagging: %p%"), count])
        for r in xrange(rows):
            item = self.model.item(r, 0)
            if item is None:
                continue
            if item and item.text() == "":
                continue

            dirName = self.model.item(r, 0).text()
            tagName = self.model.item(r, 1).text()
            tagValue = self.model.item(r, 2).text()

            self.arguments[:] = []

            if self.configFile != "":
                self.arguments.append("-config")
                self.arguments.append(self.configFile)

            self.arguments.append("-%s=%s" % (tagName, tagValue))
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

        if not self.interrupted:
            self.processFinished.emit()
        else:
            self.processInterrupted.emit()

    def taggingError(self, error):
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
