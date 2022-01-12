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

from ..attributepainterdialog import attributePainterDialog

from .utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class apDockWidgetTest(unittest.TestCase):
    """Test dockwidget works."""

    def setUp(self):
        """Runs before each test."""
        self.dockwidget = attributePainterDialog(None)

    def tearDown(self):
        """Runs after each test."""
        self.dockwidget = None

    def test_dockwidget_ok(self):
        """Test we can click OK."""
        self.dockwidget.PickSource.click()
        pass

if __name__ == "__main__":
    suite = unittest.makeSuite(apDockWidgetTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

