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

from qgis.PyQt.QtWidgets import QDockWidget
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsVectorLayer)

from .utilities import get_qgis_app

QGIS_APP = get_qgis_app()

from qgis.utils import plugins

import os


class apPluginTest(unittest.TestCase):
    """Test dockwidget works."""

    def setUp(self):
        """Runs before each test."""
        self.plugin = plugins["attributepainter"]
        self.vector_driver = QgsVectorLayer(os.path.join(self.plugin.plugin_dir,"test","testdata.gpkg|layername=testdata"),"testdata","ogr")

    def tearDown(self):
        """Runs after each test."""
        self.vector_driver = None

    def test_plugin_loaded(self):
        """Test plugin loaded"""
        self.assertTrue(self.plugin)

    def test_layer_ok(self):
        """Test testdata layer loaded"""
        self.assertTrue(self.vector_driver)

if __name__ == "__main__":
    suite = unittest.makeSuite(apPluginTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

