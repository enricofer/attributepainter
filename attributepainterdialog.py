# -*- coding: utf-8 -*-
"""
/***************************************************************************
 attributePainterDialog
                                 A QGIS plugin
 Plugin for easy replication of attributes between features
                             -------------------
        begin                : 2014-03-11
        copyright            : (C) 2014 by Enrico Ferreguti
        email                : enricofer@me.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import QtWidgets, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_attributepainter.ui'))

class attributePainterDialog(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, iface):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)