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
        self.layerHighlighted = None
        self.sourceFeat = None
        #setting dock view buttons behavior
        self.dock.PickSource.clicked.connect(self.selectSource)
        self.dock.ResetSource.clicked.connect(self.resetSource)
        self.dock.PickDestination.clicked.connect(self.applyToDestination)
        self.dock.PickDestination.setDisabled(True)
        self.dock.checkBox.clicked.connect(self.selectAllCheckbox)
        self.dock.tableWidget.setColumnCount(3)
        self.initTable()
        self.iface.legendInterface().currentLayerChanged.connect(self.checkOnLayerChange)
        self.iface.addDockWidget( Qt.LeftDockWidgetArea, self.apdockwidget )
        self.iface.projectRead.connect(self.resetSource)
        self.iface.newProjectCreated.connect(self.resetSource)
        #Call reset procedure to initialize widget
        self.dock.tableWidget.itemChanged.connect(self.highLightCellOverride)
        self.resetSource()

    #select or deselect items in qtablewidget on "select all attributes" checkbox clicked
    def selectAllCheckbox(self):
        for rowTabWidget in range(0,self.dock.tableWidget.rowCount()):
            self.dock.tableWidget.item(rowTabWidget,0).setCheckState(self.dock.checkBox.checkState())

    def initTable(self):
        self.dock.tableWidget.setHorizontalHeaderItem(0,QTableWidgetItem("  "))
        self.dock.tableWidget.setHorizontalHeaderItem(1,QTableWidgetItem("FIELD"))
        self.dock.tableWidget.setHorizontalHeaderItem(2,QTableWidgetItem("VALUE"))
        

    #source feauture selection procedure
    def selectSource(self): 
        if self.canvas.currentLayer().type() != QgsMapLayer.VectorLayer:
            return
        #test if in currentlayer there are selected features
        if (self.canvas.layers()!=[] and self.canvas.currentLayer().selectedFeatures() != []):
            if self.layerHighlighted:
                self.resetSource()
            self.dock.tableWidget.itemChanged.disconnect(self.highLightCellOverride)
            #take first selected feature as source feature
            self.sourceFeat = self.canvas.currentLayer().selectedFeatures()[0]
            self.iface.activeLayer().removeSelection() 
            #hightlight source feature with rubberband
            self.sourceEvid.setToGeometry(self.sourceFeat.geometry(),self.canvas.currentLayer())
            #get current layer attributes labels list
            field_names = [field.name() for field in self.canvas.currentLayer().pendingFields()]
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
            #catch editing signals on current layer
            #self.canvas.currentLayer().editingStarted.connect(self.checkEditable)
            #self.canvas.currentLayer().editingStopped.connect(self.checkEditable)
            #self.layerHighlighted = self.canvas.currentLayer()
            #self.checkEditable()
            #procedure to recover same field selection if current source feature has the same layer of the precedent one
            if self.canvas.currentLayer().id() != self.activeLayer:
                self.sourceAttrs={}
                self.activeLayer = self.canvas.currentLayer().id()
            else:
                for Attr in self.sourceAttrs:
                    self.dock.tableWidget.item(Attr,0).setCheckState(Qt.Checked)
            #Enable button to apply or reset
            #self.dock.PickDestination.setEnabled(True)
            self.dock.ResetSource.setEnabled(True)
            self.dock.tableWidget.itemChanged.connect(self.highLightCellOverride)
            self.checkOnLayerChange(self.canvas.currentLayer())
        else:
            print "nothing selected"

    #landing method on cell value change
    def highLightCellOverride(obj,item):
        if item.column() == 2:
            item.setBackgroundColor (QColor(183,213,225))
            #item.setForeground (QBrush(QColor(255,0,0)))

    #landing method on current layer change
    def checkOnLayerChange(self,cLayer):
        if cLayer and cLayer.type() == QgsMapLayer.VectorLayer:
            if self.layerHighlighted:
                self.layerHighlighted.editingStarted.disconnect(self.checkEditable)
                self.layerHighlighted.editingStopped.disconnect(self.checkEditable)
            if cLayer:
                self.layerHighlighted = cLayer
                self.checkEditable()
                cLayer.editingStarted.connect(self.checkEditable)
                cLayer.editingStopped.connect(self.checkEditable)
    
    #method to highlight compatible field on selected feature (even on different layer)
    def highlightCompatibleFields(self):
        if self.dock.tableWidget.rowCount()>0:
            field_names = [field.name() for field in self.canvas.currentLayer().pendingFields()]
            self.dock.tableWidget.itemChanged.disconnect(self.highLightCellOverride)
            for row in range (0,self.dock.tableWidget.rowCount()):
                if self.dock.tableWidget.item(row,1).text() in field_names:
                    self.dock.tableWidget.item(row,1).setForeground(QBrush(QColor(0,0,0)))
                    self.dock.tableWidget.item(row,2).setForeground(QBrush(QColor(0,0,0)))
                else:
                    self.dock.tableWidget.item(row,1).setForeground(QBrush(QColor(130,130,130)))
                    self.dock.tableWidget.item(row,2).setForeground(QBrush(QColor(130,130,130)))
            self.dock.tableWidget.itemChanged.connect(self.highLightCellOverride)

    #method to enable or disable apply to destination button
    def checkEditable(self):
        if self.layerHighlighted:
            self.highlightCompatibleFields()
            if self.layerHighlighted.isEditable() and self.sourceFeat:
                self.dock.PickDestination.setEnabled(True)
            else:
                self.dock.PickDestination.setDisabled(True)
    
    #method to clear source and reset attribute table
    def resetSource(self):
        self.dock.tableWidget.itemChanged.disconnect(self.highLightCellOverride)
        self.doReset()
        #if self.canvas.layers()!=[]:
        #    self.iface.activeLayer().removeSelection()
        self.dock.tableWidget.itemChanged.connect(self.highLightCellOverride)

    #method to clear source and reset attribute table
    def doReset(self):
        #if self.layerHighlighted:
        #    self.layerHighlighted.editingStarted.disconnect(self.editingChanged)
        #    self.layerHighlighted.editingStopped.disconnect(self.editingChanged)
        #    self.layerHighlighted = None
        self.dock.PickDestination.setDisabled(True)
        #clear source highlight
        self.sourceEvid.reset()
        #clear source definition
        self.sourceFeat = None
        self.sourceAttrs={}
        self.activeLayer = ""
        self.layerHighlighted = None
        #clear dock widget
        #self.dock.tableWidget.clear()
        while self.dock.tableWidget.rowCount()>0:
            self.dock.tableWidget.removeRow(0)
        self.dock.PickDestination.setEnabled(False)
        self.dock.ResetSource.setEnabled(False)

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
                    self.sourceAttrs.update({rowTabWidget:[self.dock.tableWidget.item(rowTabWidget,1).data(Qt.DisplayRole),self.dock.tableWidget.item(rowTabWidget,2).data(Qt.DisplayRole)]})
            #apply source attribute values to selected destination features
            for f in self.canvas.currentLayer().selectedFeatures():
                #self.canvas.currentLayer().dataProvider().changeAttributeValues({f.id():self.sourceAttrs})
                #self.canvas.currentLayer().changeAttributeValues({f.id():self.sourceAttrs})
                for attrId,attrValue in self.sourceAttrs.items():
                    #self.canvas.currentLayer().changeAttributeValue(f.id(),attrId,attrValue[1])
                    #print attrId,attrValue[0],attrValue[1]
                    try:
                        f[attrValue[0]]=attrValue[1]
                        self.canvas.currentLayer().updateFeature(f)
                    except:
                        pass
            self.iface.activeLayer().removeSelection() 
        else:
            print "nothing selected"

    #Remove the plugin widget and clear source feature highlight
    def unload(self):
        if self.sourceFeat:
            self.sourceEvid.reset()
        self.iface.removeDockWidget( self.apdockwidget)
        sip.delete(self.apdockwidget)
        self.apdockwidget = None

