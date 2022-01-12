# coding=utf-8
"""DockWidget test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'ef@ef.ef'
__date__ = '2022-01-12'
__copyright__ = 'Copyright 2022, enricofer@gmail.com'

import unittest
from ..attributepainter import attributePainter

from qgis.PyQt.QtWidgets import QDockWidget
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsVectorLayer)

from .utilities import get_qgis_app

QGISAPP, CANVAS, IFACE, PARENT = get_qgis_app()

from ..attributepainter import attributePainter

import os


class apPluginTest(unittest.TestCase):
    """Test dockwidget works."""

    def setUp(self):
        """Runs before each test."""
        self.plugin = attributePainter(IFACE)
        self.vector = QgsVectorLayer(os.path.join(self.plugin.plugin_dir,"test","testdata.gpkg|layername=testdata"),"testdata","ogr")

    def tearDown(self):
        """Runs after each test."""
        self.vector = None

    def test_plugin_loaded(self):
        """Test plugin loaded"""
        self.assertEqual(type(self.plugin),attributePainter)

    def test_layer_ok(self):
        """Test testdata layer loaded"""
        self.assertTrue(self.vector)

    def test_load_source(self):
        """Test source loaded"""
        self.plugin.initGui()
        feature = self.vector.getFeature(0)
        self.plugin.setSourceFeature(self.vector, feature)
        self.assertTrue(self.plugin.selectedFeature)

if __name__ == "__main__":
    suite = unittest.makeSuite(apPluginTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

