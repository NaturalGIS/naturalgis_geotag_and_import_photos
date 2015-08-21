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

import geotagphotos_utils as utils

from ui.ui_settingsdialogbase import Ui_Dialog


class SettingsDialog(QDialog, Ui_Dialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        self.btnSelectBinary.clicked.connect(self.selectExifToolPath)
        self.btnSelectConfig.clicked.connect(self.selectExifToolConfig)

        self.manageGui()

    def manageGui(self):
        self.leExifToolPath.setText(utils.getExifToolPath())
        self.leConfigPath.setText(utils.getConfigPath())

    def selectExifToolPath(self):
        dirName = QFileDialog.getExistingDirectory(None,
                                                   self.tr("Select directory"),
                                                   "",
                                                   QFileDialog.ShowDirsOnly
                                                  )
        if dirName == "":
            return

        self.leExifToolPath.setText(dirName)

    def selectExifToolConfig(self):
        settings = QSettings("Faunalia", "Geotagphotos")
        lastDir = settings.value("ui/lastConfigDir", "")
        fileName = QFileDialog.getOpenFileName(None,
                                               self.tr("Select config"),
                                               lastDir,
                                               self.tr("All files (*)")
                                              )
        if fileName == "":
            return

        self.leConfigPath.setText(fileName)

    def accept(self):
        utils.setExifToolPath(self.leExifToolPath.text())
        utils.setConfigPath(self.leConfigPath.text())
        QDialog.accept(self)
