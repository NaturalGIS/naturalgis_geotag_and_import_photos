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
import ConfigParser

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui.ui_aboutdialogbase import Ui_Dialog

import resources_rc


class AboutDialog(QDialog, Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.btnHelp = self.buttonBox.button(QDialogButtonBox.Help)

        self.lblLogo.setPixmap(QPixmap(":/icons/geotagphotos.png"))

        cfg = ConfigParser.SafeConfigParser()
        cfg.read(os.path.join(os.path.dirname(__file__), "metadata.txt"))
        version = cfg.get("general", "version")

        self.lblVersion.setText(self.tr("Version: %s") % (version))
        doc = QTextDocument()
        doc.setHtml(self.getAboutText())
        self.textBrowser.setDocument(doc)
        self.textBrowser.setOpenExternalLinks(True)

        self.buttonBox.helpRequested.connect(self.openHelp)

    def reject(self):
        QDialog.reject(self)

    def openHelp(self):
        overrideLocale = bool(QSettings().value("locale/overrideFlag", False))
        if not overrideLocale:
            localeFullName = QLocale.system().name()
        else:
            localeFullName = QSettings().value("locale/userLocale", "")

        localeShortName = localeFullName[0:2]
        if localeShortName in ["ru", "uk"]:
            QDesktopServices.openUrl(QUrl("https://github.com/NaturalGIS/geotag_and_import_photos/wiki"))
        else:
            QDesktopServices.openUrl(QUrl("https://github.com/NaturalGIS/geotag_and_import_photos/wiki"))

    def getAboutText(self):
        return self.tr("""<p>Tag and GeoTag photos and import them as a point vector layer.</p>
    <p>Plugin developed by Alexander Bruy for NaturalGIS (<a href="http://www.naturalgis.pt">http://www.naturalgis.pt</a>)</p>
    <p>NOTE: Geo-Tagging and Tagging capabilities rely on an external software
    called exiftool (<a href="http://www.sno.phy.queensu.ca/~phil/exiftool/">http://www.sno.phy.queensu.ca/~phil/exiftool/)</a></p>
    <p><strong>Homepage</strong>: <a href="https://github.com/NaturalGIS/geotag_and_import_photos">https://github.com/NaturalGIS/geotag_and_import_photos</a></p>
    <p>Please report bugs at <a href="https://github.com/NaturalGIS/geotag_and_import_photos/issues">bugtracker</a>.</p>
    """)
