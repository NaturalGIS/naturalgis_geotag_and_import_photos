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


class ImportThread(QThread):
    rangeChanged = pyqtSignal(list)
    updateProgress = pyqtSignal()
    processFinished = pyqtSignal(bool)
    processInterrupted = pyqtSignal()

    wildcards = [".jpg", ".jpeg", ".JPG", ".JPEG"]
    geotags = [u"EXIF:GPSLatitude", u"EXIF:GPSLatitudeRef", u"EXIF:GPSLongitude", u"EXIF:GPSLongitudeRef"]

    def __init__(self, photosDir, recurseDir, tagsList, outFileName, outEncoding, appendFile, config):
        QThread.__init__(self, QThread.currentThread())
        self.mutex = QMutex()
        self.stopMe = 0
        self.interrupted = False

        self.photosDir = photosDir
        self.recurseDir = recurseDir
        self.tagsList = tagsList
        self.outFileName = outFileName
        self.outEncoding = outEncoding
        self.appendFile = appendFile
        self.config = config

    def run(self):
        if self.appendFile:
            layer = self.openExistingLayer()
        else:
            layer = self.createNewLayer()

        provider = layer.dataProvider()
        fields = provider.fields()

        if not set(self.tagsList).issuperset(self.geotags):
            self.tagsList.extend(self.geotags)

        etPath = utils.getExifToolPath()
        if etPath != "":
            etPath = os.path.join(os.path.normpath(unicode(etPath)), "exiftool")
        else:
            etPath = "exiftool"

        # config file
        if self.config != "":
            etPath += " -config " + unicode(self.config)

        et = exiftool.ExifTool(etPath)

        filters = QDir.Files | QDir.NoSymLinks | QDir.NoDotAndDotDot
        nameFilter = ["*.jpg", "*.jpeg", "*.JPG", "*.JPEG"]

        count = 0

        with et:
            for root, dirs, files in os.walk(unicode(self.photosDir)):
                fileCount = len(QDir(root).entryList(nameFilter, filters))
                if fileCount > 0:
                    self.rangeChanged.emit([self.tr("Import: %p%"), fileCount])
                    for f in files:
                        if os.path.splitext(f)[1] not in self.wildcards:
                            continue
                        fName = os.path.normpath(os.path.join(root, f))
                        md = et.get_tags(self.tagsList, unicode(fName))

                        # create new feature
                        ft = QgsFeature()
                        ft.setFields(fields)

                        for k, v in md.iteritems():
                            tagName = k.replace("EXIF:", "")
                            if tagName in self.tagFieldMap.keys():
                                ft[self.tagFieldMap[tagName]] = unicode(v)

                        # hardcoded fields
                        if "filepath" in self.fieldNames:
                            ft["filepath"] = os.path.join(root, f)
                        if "filename" in self.fieldNames:
                            ft["filename"] = f

                        # get geometry
                        if not set(md.keys()).issuperset(self.geotags):
                            pass
                        else:
                            lat = float(md["EXIF:GPSLatitude"])
                            lon = float(md["EXIF:GPSLongitude"])
                            if md["EXIF:GPSLongitudeRef"] == "W":
                                lon = 0 - lon
                            if md["EXIF:GPSLatitudeRef"] == "S":
                                lat = 0 - lat

                            ft.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
                            count += 1

                        if ft.geometry() is not None:
                            provider.addFeatures([ft])

                        self.updateProgress.emit()

                        self.mutex.lock()
                        s = self.stopMe
                        self.mutex.unlock()
                        if s == 1:
                            self.interrupted = True
                            break

                if not self.recurseDir:
                    break

        haveShape = True
        if count == 0:
            if not self.appendFile:
                QgsVectorFileWriter.deleteShapeFile(self.outFileName)
            haveShape = False

        if not self.interrupted:
            self.processFinished.emit(haveShape)
        else:
            self.processInterrupted.emit()

    def createNewLayer(self):
        self.tagFieldMap = dict()
        fields = QgsFields()
        self.fieldNames = []

        # hardcoded fields
        fields.append(QgsField("filepath", QVariant.String, "", 255))
        self.fieldNames.append("filepath")
        fields.append(QgsField("filename", QVariant.String, "", 255))
        self.fieldNames.append("filename")

        for tag in self.tagsList:
            tagName = tag.replace("EXIF:", "")

            fName = utils.createUniqueFieldName(tagName, self.fieldNames)

            fields.append(QgsField(fName, QVariant.String, "", 80))
            self.fieldNames.append(fName)
            self.tagFieldMap[tagName] = fName

        crs = QgsCoordinateReferenceSystem(4326)
        shapeWriter = QgsVectorFileWriter(self.outFileName, self.outEncoding, fields, QGis.WKBPoint, crs)
        del shapeWriter

        layer = QgsVectorLayer(self.outFileName, QFileInfo(self.outFileName).baseName(), "ogr")

        return layer

    def openExistingLayer(self):
        layer = QgsVectorLayer(self.outFileName, QFileInfo(self.outFileName).baseName(), "ogr")
        fMap = layer.dataProvider().fieldNameMap()
        fNames = fMap.keys()
        self.fieldNames = ["filepath", "filename"]

        self.tagFieldMap = dict()
        for tag in self.tagsList:
            tagName = tag.replace("EXIF:", "")

            fName = utils.createUniqueFieldName(tagName, self.fieldNames)

            if fName in fNames:
                self.tagFieldMap[tagName] = fName
                self.fieldNames.append(fName)

        return layer

    def stop(self):
        self.mutex.lock()
        self.stopMe = 1
        self.mutex.unlock()

        QThread.wait(self)
