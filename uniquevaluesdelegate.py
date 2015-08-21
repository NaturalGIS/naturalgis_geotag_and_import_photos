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

from ui.ui_uniquevaluesselectorbase import Ui_UniqueValuesSelector


class UniqueValuesDelegate(QItemDelegate):
    def __init__(self, layer, field, parent=None):
        QItemDelegate.__init__(self, parent)
        self.layer = layer
        self.field = field

    def createEditor(self, parent, options, index):
        return UniqueValuesSelector(self.layer, self.field, parent)

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setText(value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.EditRole)

    def eventFilter(self, editor, event):
        if event.type() == QEvent.FocusOut and hasattr(editor, 'canFocusOut'):
            if not editor.canFocusOut:
                return False
        return QItemDelegate.eventFilter(self, editor, event)


class UniqueValuesSelector(QWidget, Ui_UniqueValuesSelector):
    def __init__(self, layer, field, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        provider = layer.dataProvider()
        idx = provider.fieldNameIndex(field)
        values = layer.dataProvider().uniqueValues(idx)
        for v in values:
            self.comboBox.addItem(unicode(v))

    def text(self):
        return self.comboBox.currentText()

    def setText(self, value):
        self.comboBox.setEditText(value)
