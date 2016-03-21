# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/enrico/Dropbox/dev/attributePainter/ui_attributepainter.ui'
#
# Created: Mon Mar 21 21:53:50 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AttributePainterForm(object):
    def setupUi(self, AttributePainterForm):
        AttributePainterForm.setObjectName(_fromUtf8("AttributePainterForm"))
        AttributePainterForm.resize(300, 357)
        AttributePainterForm.setMinimumSize(QtCore.QSize(300, 300))
        AttributePainterForm.setMaximumSize(QtCore.QSize(300, 450))
        self.verticalLayout = QtGui.QVBoxLayout(AttributePainterForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.PickSource = QtGui.QPushButton(AttributePainterForm)
        self.PickSource.setCheckable(True)
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
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.PickDestination = QtGui.QPushButton(AttributePainterForm)
        self.PickDestination.setObjectName(_fromUtf8("PickDestination"))
        self.horizontalLayout.addWidget(self.PickDestination)
        self.PickApply = QtGui.QPushButton(AttributePainterForm)
        self.PickApply.setCheckable(True)
        self.PickApply.setObjectName(_fromUtf8("PickApply"))
        self.horizontalLayout.addWidget(self.PickApply)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AttributePainterForm)
        QtCore.QMetaObject.connectSlotsByName(AttributePainterForm)

    def retranslateUi(self, AttributePainterForm):
        AttributePainterForm.setWindowTitle(_translate("AttributePainterForm", "Form", None))
        self.PickSource.setText(_translate("AttributePainterForm", "Pick source feature", None))
        self.checkBox.setText(_translate("AttributePainterForm", "Select all attributes", None))
        self.ResetSource.setText(_translate("AttributePainterForm", "Reset source", None))
        self.PickDestination.setText(_translate("AttributePainterForm", "Apply  to selection", None))
        self.PickApply.setText(_translate("AttributePainterForm", "Pick to Apply", None))

