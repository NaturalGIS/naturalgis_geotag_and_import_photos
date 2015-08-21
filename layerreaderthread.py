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

from qgis.core import *

import geotagphotos_utils as utils


class LayerReaderThread(QThread):
    rangeChanged = pyqtSignal(list)
    updateProgress = pyqtSignal(list)
    processFinished = pyqtSignal()
    processInterrupted = pyqtSignal()

    def __init__(self, layer, fieldName):
        QThread.__init__(self, QThread.currentThread())
        self.mutex = QMutex()
        self.stopMe = 0
        self.interrupted = False

        self.layer = layer
        self.fieldName = fieldName

    def run(self):
        self.mutex.lock()
        self.stopMe = 0
        self.mutex.unlock()

        index = self.layer.fieldNameIndex(self.fieldName)
        request = QgsFeatureRequest()
        request.setSubsetOfAttributes([index])

        count = self.layer.featureCount()
        self.rangeChanged.emit([self.tr(""), count])

        for ft in self.layer.getFeatures(request):
            geom = QgsGeometry(ft.geometry()).asPoint()
            attrValue = ft[index]

            self.updateProgress.emit([attrValue, geom.x(), geom.y()])

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

    def stop(self):
        self.mutex.lock()
        self.stopMe = 1
        self.mutex.unlock()

        QThread.wait(self)
