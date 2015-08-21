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
# Software Foundation, either version 2 of the License, or (at your option)
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
import locale
import platform
import subprocess

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *


def getVectorLayerNames():
    layerMap = QgsMapLayerRegistry.instance().mapLayers()
    layerNames = []
    for name, layer in layerMap.iteritems():
        if layer.type() == QgsMapLayer.VectorLayer and layer.wkbType() in [QGis.WKBPoint, QGis.WKBPoint25D]:
            layerNames.append(unicode(layer.name()))
    return sorted(layerNames, cmp=locale.strcoll)


def getVectorLayerByName(layerName):
    layerMap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layerMap.iteritems():
        if layer.type() == QgsMapLayer.VectorLayer and layer.name() == layerName:
            if layer.isValid():
                return layer
            else:
                return None


def getFieldNames(layer):
    fields = layer.pendingFields()
    fieldNames = []
    for field in fields:
        if not field.name() in fieldNames:
            fieldNames.append(unicode(field.name()))
    return sorted(fieldNames, cmp=locale.strcoll)


def getFieldType(layer, fieldName):
    fields = layer.pendingFields()
    for field in fields:
        if field.name() == fieldName:
            return field.typeName()


def createUniqueFieldName(fieldName, fieldList):
    shortName = fieldName[:10]

    if len(fieldList) == 0:
        return shortName

    if shortName not in fieldList:
        return shortName

    shortName = fieldName[:8] + "_1"
    changed = True
    while changed:
        changed = False
        for n in fieldList:
            if n == shortName:
                # create unique field name
                num = int(shortName[-1:])
                if num < 9:
                    shortName = shortName[:8] + "_" + str(num + 1)
                else:
                    shortName = shortName[:7] + "_" + str(num + 1)

                changed = True

    return shortName


def saveDialog(parent):
    settings = QSettings()
    dirName = settings.value("/UI/lastShapefileDir")
    filtering = "Shapefiles (*.shp)"
    encoding = settings.value("/UI/encoding")
    title = QCoreApplication.translate("ImportPhotosDialog", "Select output shapefile")

    fileDialog = QgsEncodingFileDialog(parent, title, dirName, filtering, encoding)
    fileDialog.setDefaultSuffix("shp")
    fileDialog.setFileMode(QFileDialog.AnyFile)
    fileDialog.setAcceptMode(QFileDialog.AcceptSave)
    fileDialog.setConfirmOverwrite(True)

    if not fileDialog.exec_() == QDialog.Accepted:
        return None, None

    files = fileDialog.selectedFiles()
    settings.setValue("/UI/lastShapefileDir", QFileInfo(unicode(files[0])).absolutePath())
    return (unicode(files[0]), unicode(fileDialog.encoding()))


def setExifToolPath(toolPath):
    settings = QSettings("Faunalia", "Geotagphotos")
    settings.setValue("tools/exifToolPath", toolPath)


def getExifToolPath():
    settings = QSettings("Faunalia", "Geotagphotos")
    return settings.value("tools/exifToolPath", "")


def setConfigPath(configPath):
    settings = QSettings("Faunalia", "Geotagphotos")
    settings.setValue("tools/exifToolConfig", configPath)


def getConfigPath():
    settings = QSettings("Faunalia", "Geotagphotos")
    return settings.value("tools/exifToolConfig", "")


def setProcessEnvironment(process):
    envVariables = {"PATH" : getExifToolPath()}

    sep = os.pathsep

    for name, value in envVariables.iteritems():
        if value is None or value == "":
            continue

        envVal = os.getenv(name)
        if envVal is None or envVal == "":
            envVal = str(value)
        elif (platform.system() == "Windows" and value.lower() not in envVal.lower().split(sep)) or \
             (platform.system() != "Windows" and value not in envVal.split(sep)):
            envVal += "%s%s" % (sep, os.path.normpath(unicode(value)))
        else:
            envVal = None

        if envVal is not None:
            os.putenv(name, envVal)


def exiftoolInstalled():
    etPath = getExifToolPath()
    if not etPath == "":
        etPath = os.path.join(os.path.normpath(unicode(etPath)), "exiftool")
    else:
        etPath = "exiftool"

    res = 1
    fnull = open(os.devnull, "w")
    try:
        res = subprocess.call(etPath, stdin=fnull, stdout=fnull, stderr=fnull)
    except:
        pass
    finally:
        fnull.close()

    return res == 0
