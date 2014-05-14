# -*- coding: utf-8 -*-
"""
/***************************************************************************
 attributePainter
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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load attributePainter class from file attributePainter
    from attributepainter import attributePainter
    return attributePainter(iface)
