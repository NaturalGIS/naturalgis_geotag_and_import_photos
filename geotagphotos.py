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

import geotagphotosdialog
import importphotosdialog
import tagphotosdialog
import settingsdialog
import aboutdialog

import resources_rc


class GeotagPhotosPlugin:
    def __init__(self, iface):
        self.iface = iface

        self.qgsVersion = unicode(QGis.QGIS_VERSION_INT)

        # For i18n support
        userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/geptagphotos"
        systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/geptagphotos"

        overrideLocale = bool(QSettings().value("locale/overrideFlag", False))
        if not overrideLocale:
            localeFullName = QLocale.system().name()
        else:
            localeFullName = QSettings().value("locale/userLocale", "")

        if QFileInfo(userPluginPath).exists():
            translationPath = userPluginPath + "/i18n/geotagphotos_" + localeFullName + ".qm"
        else:
            translationPath = systemPluginPath + "/i18n/geotagphotos_" + localeFullName + ".qm"

        self.localePath = translationPath
        if QFileInfo(self.localePath).exists():
            self.translator = QTranslator()
            self.translator.load(self.localePath)
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        if int(self.qgsVersion) < 10900:
            qgisVersion = self.qgsVersion[0] + "." + self.qgsVersion[2] + "." + self.qgsVersion[3]
            QMessageBox.warning(self.iface.mainWindow(), "Geotag and import photos",
                                QCoreApplication.translate("Geotag and import photos", "QGIS %s detected.\n") % (qgisVersion) +
                                QCoreApplication.translate("Geotag and import photos", "This version of Geotag and import photos requires at least QGIS version 2.0.\nPlugin will not be enabled."))
            return None

        self.actionGeotag = QAction(QIcon(":/icons/geotagphotos.png"), "Geotag photos", self.iface.mainWindow())
        self.actionGeotag.setStatusTip(QCoreApplication.translate("Geotag and import photos", "Geotag photos"))
        self.iface.registerMainWindowAction(self.actionGeotag, "Shift+G")
        self.actionTag = QAction(QIcon(":/icons/tagphotos.png"), "Tag photos", self.iface.mainWindow())
        self.actionTag.setStatusTip(QCoreApplication.translate("Geotag and import photos", "Geotag photos"))
        self.iface.registerMainWindowAction(self.actionTag, "Shift+T")
        self.actionImport = QAction(QIcon(":/icons/importphotos.png"), "Import photos", self.iface.mainWindow())
        self.actionImport.setStatusTip(QCoreApplication.translate("Geotag and import photos", "Geotag photos"))
        self.iface.registerMainWindowAction(self.actionImport, "Shift+I")
        self.actionSettings = QAction(QIcon(":/icons/settings.png"), "Settings", self.iface.mainWindow())
        self.actionSettings.setStatusTip(QCoreApplication.translate("Geotag and import photos", "Plugin settings"))
        self.actionAbout = QAction(QIcon(":/icons/about.png"), "About", self.iface.mainWindow())
        self.actionAbout.setStatusTip(QCoreApplication.translate("Geotag and import photos", "About Geotag and import photos"))

        self.actionGeotag.triggered.connect(self.geotagPhotos)
        self.actionTag.triggered.connect(self.tagPhotos)
        self.actionImport.triggered.connect(self.importPhotos)
        self.actionSettings.triggered.connect(self.settings)
        self.actionAbout.triggered.connect(self.about)

        self.iface.addPluginToVectorMenu(QCoreApplication.translate("Geotag and import photos", "Geotag and import photos"), self.actionGeotag)
        self.iface.addPluginToVectorMenu(QCoreApplication.translate("Geotag and import photos", "Geotag and import photos"), self.actionTag)
        self.iface.addPluginToVectorMenu(QCoreApplication.translate("Geotag and import photos", "Geotag and import photos"), self.actionImport)
        self.iface.addPluginToVectorMenu(QCoreApplication.translate("Geotag and import photos", "Geotag and import photos"), self.actionSettings)
        self.iface.addPluginToVectorMenu(QCoreApplication.translate("Geotag and import photos", "Geotag and import photos"), self.actionAbout)
        self.iface.addVectorToolBarIcon(self.actionGeotag)
        self.iface.addVectorToolBarIcon(self.actionTag)
        self.iface.addVectorToolBarIcon(self.actionImport)

    def unload(self):
        self.iface.unregisterMainWindowAction(self.actionGeotag)
        self.iface.unregisterMainWindowAction(self.actionImport)
        self.iface.unregisterMainWindowAction(self.actionTag)

        self.iface.removePluginVectorMenu(QCoreApplication.translate("Geotag and import photos", "Geotag and import photos"), self.actionGeotag)
        self.iface.removePluginVectorMenu(QCoreApplication.translate("Geotag and import photos", "Geotag and import photos"), self.actionImport)
        self.iface.removePluginVectorMenu(QCoreApplication.translate("Geotag and import photos", "Geotag and import photos"), self.actionTag)
        self.iface.removePluginVectorMenu(QCoreApplication.translate("Geotag and import photos", "Geotag and import photos"), self.actionSettings)
        self.iface.removePluginVectorMenu(QCoreApplication.translate("Geotag and import photos", "Geotag and import photos"), self.actionAbout)
        self.iface.removeVectorToolBarIcon(self.actionGeotag)
        self.iface.removeVectorToolBarIcon(self.actionImport)
        self.iface.removeVectorToolBarIcon(self.actionTag)

    def about(self):
        dlg = aboutdialog.AboutDialog()
        dlg.exec_()

    def geotagPhotos(self):
        dlg = geotagphotosdialog.GeotagPhotosDialog(self.iface)
        dlg.show()
        dlg.exec_()

    def importPhotos(self):
        dlg = importphotosdialog.ImportPhotosDialog(self.iface)
        dlg.show()
        dlg.exec_()

    def tagPhotos(self):
        dlg = tagphotosdialog.TagPhotosDialog(self.iface)
        dlg.show()
        dlg.exec_()

    def settings(self):
        dlg = settingsdialog.SettingsDialog(self.iface)
        dlg.exec_()
