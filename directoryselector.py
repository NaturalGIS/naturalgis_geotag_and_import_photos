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
from PyQt4.QtGui import *

from ui.ui_directoryselectorbase import Ui_DirectorySelector


class DirectorySelector(QWidget, Ui_DirectorySelector):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.canFocusOut = False

        self.setFocusPolicy(Qt.StrongFocus)
        self.btnSelect.clicked.connect(self.selectDirectory)

    def clear(self):
        self.lineEdit.clear()

    def selectDirectory(self):
        settings = QSettings("Faunalia", "Geotagphotos")
        lastDir = settings.value("ui/lastPhotosDir", "")
        dirName = QFileDialog.getExistingDirectory(None,
                                                   self.tr("Select directory"),
                                                   lastDir,
                                                   QFileDialog.ShowDirsOnly
                                                  )
        if dirName == "":
            return

        self.lineEdit.setText(dirName)
        settings.setValue("ui/lastPhotosDir", os.path.dirname(unicode(dirName)))

    def text(self):
        return self.lineEdit.text()

    def setText(self, value):
        self.lineEdit.setText(value)
