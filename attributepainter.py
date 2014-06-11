# -*- coding: utf-8 -*-
"""
/***************************************************************************
 attributePainter
                                 A QGIS plugin
 Plugin for easy replication of attributes between features
                              -------------------
        begin                : 2014-03-11
        copyright            : (C) 2014 by Enrico Ferreguti
        email                : enricofer@gmail.com
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from qgis.core import *
from qgis.utils import *
from qgis.gui import *
# Import the code for the dialog
from attributepainterdialog import attributePainterDialog
# Initialize Qt resources from file resources.py
import resources
import sip
import os.path
import os


class attributePainter:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        # Source feature rubberband definition
        colorSource = QColor(250,0,0,200)
        self.sourceEvid = QgsRubberBand(self.canvas, QGis.Line)
        self.sourceEvid.setColor(colorSource)
        self.sourceEvid.setWidth(3)


    def initGui(self):
        #creating dock view intance
        self.dock = attributePainterDialog(self.iface)
        self.apdockwidget=QDockWidget("AttributePainter" , self.iface.mainWindow() )
        self.apdockwidget.setObjectName("AttributePainter")
        self.apdockwidget.setWidget(self.dock)
        #setting dock view buttons behavior
        self.dock.PickSource.clicked.connect(self.selectSource)
        self.dock.ResetSource.clicked.connect(self.resetSource)
        self.dock.PickDestination.clicked.connect(self.applyToDestination)
        self.dock.checkBox.clicked.connect(self.selectAllCheckbox)
        self.dock.tableWidget.setColumnCount(3)
        self.dock.tableWidget.setHorizontalHeaderItem(0,QTableWidgetItem("  "))
        self.dock.tableWidget.setHorizontalHeaderItem(1,QTableWidgetItem("FIELD"))
        self.dock.tableWidget.setHorizontalHeaderItem(2,QTableWidgetItem("VALUE"))
        self.iface.addDockWidget( Qt.LeftDockWidgetArea, self.apdockwidget )
        #Call reset procedure to initialize widget
        self.dock.tableWidget.itemChanged.connect(self.highLightCellOverride)
        self.resetSource()

    #select or deselect items in qtablewidget on "select all attributes" checkbox clicked
    def selectAllCheckbox(self):
        for rowTabWidget in range(0,self.dock.tableWidget.rowCount()):
            self.dock.tableWidget.item(rowTabWidget,0).setCheckState(self.dock.checkBox.checkState())


    #source feauture selection procedure
    def selectSource(self): 
        #test if in currentlayer there are selected features
        if (self.canvas.layers()!=[] and self.canvas.currentLayer().selectedFeatures() != []):
            self.dock.tableWidget.itemChanged.disconnect(self.highLightCellOverride)
            #take first selected feature as source feature
            self.sourceFeat = self.canvas.currentLayer().selectedFeatures()[0]
            self.iface.activeLayer().removeSelection() 
            #hightlight source feature with rubberband
            self.sourceEvid.setToGeometry(self.sourceFeat.geometry(),self.canvas.currentLayer())
            #get current layer attributes labels list
            field_names = [field.name() for field in self.canvas.currentLayer().dataProvider().fields()]
            self.sourceAttrsTab=[]
            self.dock.tableWidget.setRowCount(len(field_names))
            #loading attributes labels and values in QTableWidget
            for n in range(0,len(field_names)):
                    item=QTableWidgetItem()
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Unchecked)
                    item.setText("")
                    #set first column as checkbox
                    self.dock.tableWidget.setItem(n,0,item)
                    #set second colunm as attribute label
                    self.dock.tableWidget.setItem(n,1,QTableWidgetItem(field_names[n]))
                    #set third column as attribute value
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole,self.sourceFeat.attributes()[n])
                    self.dock.tableWidget.setItem(n,2,item)
                    #self.dock.tableWidget.setItem(n,2,QTableWidgetItem(str(self.sourceFeat.attributes()[n])))
            #resize table to contents
            self.dock.tableWidget.resizeColumnsToContents()
            self.dock.tableWidget.horizontalHeader().setStretchLastSection(True)
            #procedure to recover same field selection if current source feature has the same layer of the precedent one
            if self.canvas.currentLayer().id() != self.activeLayer:
                self.sourceAttrs={}
                self.activeLayer = self.canvas.currentLayer().id()
            else:
                for Attr in self.sourceAttrs:
                    self.dock.tableWidget.item(Attr,0).setCheckState(Qt.Checked)
            #Enable button to apply or reset
            self.dock.PickDestination.setEnabled(True)
            self.dock.ResetSource.setEnabled(True)
            self.dock.tableWidget.itemChanged.connect(self.highLightCellOverride)
        else:
            print "nothing selected"

    def highLightCellOverride(obj,item):
        if item.column() == 2:
            item.setBackgroundColor (QColor(183,213,225))

    #method to clear source and reset attribute table
    def resetSource(self):
        self.dock.tableWidget.itemChanged.disconnect(self.highLightCellOverride)
        self.doReset()
        self.dock.tableWidget.itemChanged.connect(self.highLightCellOverride)

    #method to clear source and reset attribute table
    def doReset(self):
        #clear source highlight
        self.sourceEvid.reset()
        #clear source definition
        self.sourceFeat = QgsFeature()
        self.sourceAttrs={}
        self.activeLayer = ""
        #clear dock widget
        self.dock.tableWidget.clearContents()
        self.dock.PickDestination.setEnabled(False)
        self.dock.ResetSource.setEnabled(False)
        if self.canvas.layers()!=[]:
            self.iface.activeLayer().removeSelection()

    #method to apply selected fields to selected destination features
    def applyToDestination(self):
        if self.canvas.currentLayer().selectedFeatures()!=[]:
            #destFeat = self.canvas.currentLayer().selectedFeatures()
            #rebuild source attribute dict set to apply to destination features
            self.sourceAttrs={}
            for rowTabWidget in range(0,self.dock.tableWidget.rowCount()):
                rowCheckbox = self.dock.tableWidget.item(rowTabWidget,0)
                #take only selected attributes by checkbox
                if rowCheckbox.checkState() == Qt.Checked:
                    #self.sourceAttrs.update({rowTabWidget:self.sourceFeat.attributes()[rowTabWidget]})
                    self.sourceAttrs.update({rowTabWidget:self.dock.tableWidget.item(rowTabWidget,2).data(Qt.DisplayRole)})
            #apply source attribute values to selected destination features
            for f in self.canvas.currentLayer().selectedFeatures():
                self.canvas.currentLayer().dataProvider().changeAttributeValues({f.id():self.sourceAttrs})
            self.iface.activeLayer().removeSelection() 
        else:
            print "nothing selected"

    #Remove the plugin widget and clear source feature highlight
    def unload(self):
        if self.sourceFeat.isValid():
            self.sourceEvid.reset()
        self.iface.removeDockWidget( self.apdockwidget)
        sip.delete(self.apdockwidget)
        self.apdockwidget = None

