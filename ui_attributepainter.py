# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_attributepainter.ui'
#
# Created: Mon Mar 24 08:03:46 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AttributePainterForm(object):
    def setupUi(self, AttributePainterForm):
        AttributePainterForm.setObjectName(_fromUtf8("AttributePainterForm"))
        AttributePainterForm.resize(300, 300)
        AttributePainterForm.setMinimumSize(QtCore.QSize(300, 300))
        AttributePainterForm.setMaximumSize(QtCore.QSize(300, 450))
        self.verticalLayout = QtGui.QVBoxLayout(AttributePainterForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.PickSource = QtGui.QPushButton(AttributePainterForm)
        self.PickSource.setObjectName(_fromUtf8("PickSource"))
        self.verticalLayout.addWidget(self.PickSource)
        self.checkBox = QtGui.QCheckBox(AttributePainterForm)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.tableWidget = QtGui.QTableWidget(AttributePainterForm)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.tableWidget.setFont(font)
        self.tableWidget.setLineWidth(0)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(16)
        self.tableWidget.verticalHeader().setMinimumSectionSize(12)
        self.verticalLayout.addWidget(self.tableWidget)
        self.ResetSource = QtGui.QPushButton(AttributePainterForm)
        self.ResetSource.setObjectName(_fromUtf8("ResetSource"))
        self.verticalLayout.addWidget(self.ResetSource)
        self.PickDestination = QtGui.QPushButton(AttributePainterForm)
        self.PickDestination.setObjectName(_fromUtf8("PickDestination"))
        self.verticalLayout.addWidget(self.PickDestination)

        self.retranslateUi(AttributePainterForm)
        QtCore.QMetaObject.connectSlotsByName(AttributePainterForm)

    def retranslateUi(self, AttributePainterForm):
        AttributePainterForm.setWindowTitle(QtGui.QApplication.translate("AttributePainterForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.PickSource.setText(QtGui.QApplication.translate("AttributePainterForm", "Pick source feature", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("AttributePainterForm", "Select all attributes", None, QtGui.QApplication.UnicodeUTF8))
        self.ResetSource.setText(QtGui.QApplication.translate("AttributePainterForm", "Reset source", None, QtGui.QApplication.UnicodeUTF8))
        self.PickDestination.setText(QtGui.QApplication.translate("AttributePainterForm", "Apply attributes to selected features", None, QtGui.QApplication.UnicodeUTF8))

