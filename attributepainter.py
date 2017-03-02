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
from qgis.PyQt.QtCore import Qt
if False:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4 import uic
    from qgis.core import *
    from qgis.utils import *
    from qgis.gui import *
if True:
    from qgis.PyQt.QtGui import QColor, QIcon, QBrush
    from qgis.PyQt.QtWidgets import QComboBox, QDockWidget, QAction, QTableWidgetItem
    from qgis.PyQt import uic
    from qgis.core import QgsMapLayer
    from qgis.gui import QgsRubberBand
# Import the code for the dialog
from .attributepainterdialog import attributePainterDialog
from .identifygeometry import IdentifyGeometry
# Initialize Qt resources from file resources.py
#import resources
import sip
import os


class attributePainter:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # Source feature rubberband definition
        colorSource = QColor(250,0,0,200)
        self.sourceEvid = QgsRubberBand(self.canvas)
        self.sourceEvid.setColor(colorSource)
        self.sourceEvid.setWidth(3)


    def initGui(self):
        # Create action that will show plugin widget
        self.action = QAction(
            QIcon(os.path.join(self.plugin_dir,"icon.png")),
            u"AttributePainter", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)
        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&foglioMappale", self.action)
        #creating dock view intance
        self.dock = attributePainterDialog(self.iface)
        self.apdockwidget=QDockWidget("AttributePainter" , self.iface.mainWindow() )
        self.apdockwidget.setObjectName("AttributePainter")
        self.apdockwidget.setWidget(self.dock)
        self.layerHighlighted = None
        self.sourceFeat = None
        #setting dock view buttons behavior
        self.dock.PickSource.toggled.connect(self.setSourceMapTool)
        self.dock.ResetSource.clicked.connect(self.resetSource)
        self.dock.PickDestination.clicked.connect(self.applyToDestination)
        self.dock.PickDestination.setDisabled(True)
        self.dock.PickApply.setDisabled(True)
        self.dock.PickApply.toggled.connect(self.setDestinationMapTool)
        self.dock.checkBox.clicked.connect(self.selectAllCheckbox)
        self.dock.tableWidget.setColumnCount(3)
        self.initTable()
        #setting interface behaviours
        self.session = destinationLayerState()
        try:
            #QGIS2 API
            self.iface.legendInterface().currentLayerChanged.connect(self.checkOnLayerChange)
        except:
            #QGIS3 API
            self.iface.currentLayerChanged.connect(self.checkOnLayerChange)
        self.iface.addDockWidget( Qt.LeftDockWidgetArea, self.apdockwidget )
        self.iface.projectRead.connect(self.resetSource)
        self.iface.newProjectCreated.connect(self.resetSource)
        self.canvas.mapToolSet.connect(self.toggleMapTool)
        self.sourceMapTool = IdentifyGeometry(self.canvas,pickMode='selection')
        self.destinationMapTool = IdentifyGeometry(self.canvas,pickMode='active')
        self.sourceMapTool.geomIdentified.connect(self.setSourceFeature)
        self.destinationMapTool.geomIdentified.connect(self.setDestinationFeature)
        #Call reset procedure to initialize widget
        self.dock.tableWidget.itemChanged.connect(self.highLightCellOverride)
        self.resetSource()
        self.actualLayer = None

    def selectAllCheckbox(self):
        '''
        select or deselect items in qtablewidget on "select all attributes" checkbox clicked
        '''
        for rowTabWidget in range(0,self.dock.tableWidget.rowCount()):
            self.dock.tableWidget.item(rowTabWidget,0).setCheckState(self.dock.checkBox.checkState())

    def initTable(self):
        '''
        QTableWidget initialization
        '''
        self.dock.tableWidget.setHorizontalHeaderItem(0,QTableWidgetItem("  "))
        self.dock.tableWidget.setHorizontalHeaderItem(1,QTableWidgetItem("FIELD"))
        self.dock.tableWidget.setHorizontalHeaderItem(2,QTableWidgetItem("VALUE"))
        

    def setComboField(self,content,type,layer):
        '''
        returns a qcombobox loaded with compatible field names (depending on selected layer)
        '''
        combo = QComboBox();
        fieldNames = self.scanLayerFieldsNames(layer)
        fieldTypes = self.scanLayerFieldsTypes(layer)
        choices = []
        for n in range(0,len(fieldTypes)):
            if fieldTypes[n] == type:
                choices.append(fieldNames[n])
        combo.addItems(choices)
        if content in choices:
            combo.setCurrentIndex(choices.index(content))
        else:
            combo.addItem(content)
            combo.setCurrentIndex(combo.count()-1)
        combo.activated.connect(lambda: self.highlightCompatibleFields(LayerChange=None))
        return combo
        

    def scanLayerFieldsNames(self,layer):
        '''
        returns fields names as strings list
        '''
        if layer:
            return [field.name() for field in layer.pendingFields()]
        else:
            return []

    def scanLayerFieldsTypes(self,layer):
        '''
        returns fields types as qvariant list
        '''
        if layer:
            return [field.type() for field in layer.pendingFields()]
        else:
            return []

    def selectSource(self): 
        '''
        source feature selection procedure
        '''
        if self.layerHighlighted:
            self.resetSource()
        try:
            self.dock.tableWidget.itemChanged.disconnect(self.highLightCellOverride)
        except:
            pass
        #take first selected feature as source feature
        self.sourceFeat = self.selectedFeature
        #hightlight source feature with rubberband
        self.sourceEvid.setToGeometry(self.sourceFeat.geometry(),self.selectedLayer)
        #get current layer attributes labels list
        field_names = self.scanLayerFieldsNames(self.selectedLayer)
        field_types = self.scanLayerFieldsTypes(self.selectedLayer)
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
                #set second colunm as attribute label as qcombobox widget
                self.dock.tableWidget.setCellWidget(n,1,self.setComboField(field_names[n],field_types[n],self.canvas.currentLayer()))
                #set third column as attribute value
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole,self.sourceFeat.attributes()[n])
                self.dock.tableWidget.setItem(n,2,item)
        #resize table to contents
        self.dock.tableWidget.resizeColumnsToContents()
        self.dock.tableWidget.horizontalHeader().setStretchLastSection(True)
        #procedure to recover same field selection if current source feature has the same layer of the precedent one
        if self.selectedLayer.id() != self.activeLayer:
            self.sourceAttrs={}
            self.activeLayer = self.selectedLayer.id()
        else:
            for Attr in self.sourceAttrs:
                self.dock.tableWidget.item(Attr,0).setCheckState(Qt.Checked)
        #Enable button to apply or reset
        self.dock.ResetSource.setEnabled(True)
        self.dock.tableWidget.itemChanged.connect(self.highLightCellOverride)
        self.checkOnLayerChange(self.canvas.currentLayer())

    def highLightCellOverride(obj,item):
        '''
        landing method on cell value change
        '''
        if item.column() == 2:
            item.setBackground(QBrush(QColor(183,213,225)))
            #item.setForeground (QBrush(QColor(255,0,0)))

    def toggleMapTool(self,mapTool):
        '''
        landing method on canvas maptool change
        '''
        self.dock.PickSource.blockSignals(True)
        self.dock.PickApply.blockSignals(True)
        if mapTool != self.sourceMapTool and mapTool != self.destinationMapTool:
            self.dock.PickSource.setChecked(False)
            self.dock.PickApply.setChecked(False)
        elif mapTool == self.sourceMapTool:
            self.dock.PickApply.setChecked(False)
        elif mapTool == self.destinationMapTool:
            self.dock.PickSource.setChecked(False)
        self.dock.PickSource.blockSignals(False)
        self.dock.PickApply.blockSignals(False)

    def checkOnLayerChange(self,cLayer):
        '''
        landing method on current layer change
        '''
        if cLayer and cLayer.type() == QgsMapLayer.VectorLayer:
            self.session.backupState(self.layerHighlighted, self.dock.tableWidget)
            # Restore a session for the current layer or custom table items to it
            if self.layerHighlighted:
                self.layerHighlighted.editingStarted.disconnect(self.checkEditable)
                self.layerHighlighted.editingStopped.disconnect(self.checkEditable)
            if cLayer:
                self.layerHighlighted = cLayer
                self.checkEditable()
                cLayer.editingStarted.connect(self.checkEditable)
                cLayer.editingStopped.connect(self.checkEditable)
            self.session.restoreState(cLayer,self.dock.tableWidget)
    
    def highlightCompatibleFields(self, LayerChange = True):
        '''
        method to highlight compatible field on selected feature (even on different layer)
        '''
        if self.dock.tableWidget.rowCount()>0:
            source_field_names = self.scanLayerFieldsNames(self.selectedLayer)
            source_field_types = self.scanLayerFieldsTypes(self.selectedLayer)
            destination_field_names = self.scanLayerFieldsNames(self.canvas.currentLayer())
            self.dock.tableWidget.itemChanged.disconnect(self.highLightCellOverride)
            for row in range (0,self.dock.tableWidget.rowCount()):
                if LayerChange:
                    self.dock.tableWidget.setCellWidget(row,1,self.setComboField(source_field_names[row],source_field_types[row],self.canvas.currentLayer()))
                if self.dock.tableWidget.cellWidget(row,1).currentText() in destination_field_names:
                    #self.dock.tableWidget.item(row,1).setForeground(QBrush(QColor(0,0,0)))
                    self.dock.tableWidget.item(row,2).setForeground(QBrush(QColor(0,0,0)))
                else:
                    #self.dock.tableWidget.item(row,1).setForeground(QBrush(QColor(130,130,130)))
                    self.dock.tableWidget.item(row,2).setForeground(QBrush(QColor(130,130,130)))
            self.dock.tableWidget.itemChanged.connect(self.highLightCellOverride)

    def checkEditable(self):
        '''
        method to enable or disable apply to destination button
        '''
        if self.layerHighlighted:
            self.highlightCompatibleFields()
            if self.layerHighlighted.isEditable() and self.sourceFeat:
                self.dock.PickDestination.setEnabled(True)
                self.dock.PickApply.setEnabled(True)
            else:
                self.dock.PickDestination.setDisabled(True)
                self.dock.PickApply.setDisabled(True)
    
    def resetSource(self):
        '''
        method to clear source and reset attribute table
        '''
        self.dock.tableWidget.itemChanged.disconnect(self.highLightCellOverride)
        self.doReset()
        #if self.canvas.layers()!=[]:
        #    self.iface.activeLayer().removeSelection()
        self.dock.tableWidget.itemChanged.connect(self.highLightCellOverride)

    def doReset(self):
        '''
        method to clear source and reset attribute table
        '''
        self.dock.PickDestination.setDisabled(True)
        #clear source highlight
        self.sourceEvid.reset()
        #clear source definition
        self.sourceFeat = None
        self.sourceAttrs={}
        self.activeLayer = "nn"
        self.session.removeState(self.canvas.currentLayer())
        self.layerHighlighted = None
        #clear dock widget
        while self.dock.tableWidget.rowCount()>0:
            self.dock.tableWidget.removeRow(0)
        self.dock.PickDestination.setEnabled(False)
        self.dock.ResetSource.setEnabled(False)

    def applyToDestination(self):
        '''
        method to apply selected fields to selected destination features
        '''
        if self.canvas.currentLayer().selectedFeatures()!=[]:
            self.sourceAttributes = self.getSourceAttrs()
            #apply source attribute values to selected destination features
            for f in self.canvas.currentLayer().selectedFeatures():
                self.applyToFeature(f,self.sourceAttributes)
            self.iface.activeLayer().removeSelection() 
        else:
            pass
            #print ("nothing selected")

    def getSourceAttrs(self):
        '''
        rebuild source attribute dict set to apply to destination features
        '''
        sourceAttrs={}
        for rowTabWidget in range(0,self.dock.tableWidget.rowCount()):
            rowCheckbox = self.dock.tableWidget.item(rowTabWidget,0)
            #take only checked attributes
            if rowCheckbox.checkState() == Qt.Checked:
                sourceAttrs.update({rowTabWidget:[self.dock.tableWidget.cellWidget(rowTabWidget,1).currentText(),self.dock.tableWidget.item(rowTabWidget,2).data(Qt.DisplayRole)]})
        return sourceAttrs

    def applyToFeature(self,feature,sourceSet):
        '''
        method to apply destination fields cyclying between feature fields
        '''
        #print (sourceSet.items())
        for attrId,attrValue in sourceSet.items():
            try:
                feature[attrValue[0]]=attrValue[1]
                self.canvas.currentLayer().updateFeature(feature)
            except:
                pass

    def run(self):
        '''
        show/hide the widget
        '''
        if self.apdockwidget.isVisible():
            self.apdockwidget.hide()
            self.resetSource()
        else:
            self.apdockwidget.show()

    def unload(self):
        '''
        Remove the plugin widget and clear source feature highlight
        '''
        if self.sourceFeat:
            self.sourceEvid.reset()
        self.iface.removeToolBarIcon(self.action)
        self.iface.removeDockWidget(self.apdockwidget)
        self.canvas.mapToolSet.disconnect(self.toggleMapTool)
        try:
            self.iface.legendInterface().currentLayerChanged.disconnect(self.checkOnLayerChange)
        except:
            self.iface.currentLayerChanged.disconnect(self.checkOnLayerChange)
        self.iface.projectRead.disconnect(self.resetSource)

    def setSourceFeature(self, layer, feature):
        '''
        landing method on source maptool identify
        '''
        self.selectedLayer = layer
        self.selectedFeature = feature
        self.dock.PickSource.setChecked(False)
        self.canvas.setMapTool(self.oldMapTool)
        self.selectSource()

    def setDestinationFeature(self, layer, feature):
        '''
        landing method on destination maptool identify
        '''
        sourceAttributes = self.getSourceAttrs()
        self.applyToFeature(feature,sourceAttributes)

    def setSourceMapTool(self, checked):
        '''
        landing method on pick source button toggle
        '''
        if checked:
            self.oldMapTool = self.canvas.mapTool()
            self.canvas.setMapTool(self.sourceMapTool)
        else:
            self.oldMapTool = self.canvas.mapTool()

    def setDestinationMapTool(self,checked):
        '''
        landing method on pick apply button toggle
        '''
        if checked:
            self.oldMapTool = self.canvas.mapTool()
            self.canvas.setMapTool(self.destinationMapTool)
        else:
            self.canvas.setMapTool(self.oldMapTool)

class destinationLayerState:

    def __init__(self):
        self.states = {}

    def removeState(self, layer):
        if layer and layer.id() in self.states.keys():
            del self.states[layer.id()]
            return True
        else:
            return None

    def backupState(self, layer, table):
        if layer:
            stateArray = []
            for row in range (0,table.rowCount()):
                checked = table.item(row,0).checkState() == Qt.Checked
                layersMap = [table.cellWidget(row,1).itemText(i) for i in range(table.cellWidget(row,1).count())]
                currentLayer = table.cellWidget(row,1).currentIndex()
                type = table.item(row,2).type()
                value = table.item(row,2).data(Qt.DisplayRole)
                isAppliable = table.item(row,2).foreground().color().value() == QColor(0,0,0).value()
                isOverriden = table.item(row,2).background().color().value() == QColor(183,213,225).value()
                stateArray.append([checked,layersMap,currentLayer,type,value,isAppliable,isOverriden])
            self.states[layer.id()] = stateArray
            #print (self.states)

    def restoreState(self,layer,table):
        if layer.id() in self.states.keys():
            table.blockSignals(True)
            #clear dock widget
            while table.rowCount()>0:
                table.removeRow(0)
            #add rows
            table.setRowCount(len(self.states[layer.id()]))
            for n in range(0, len(self.states[layer.id()])):
                row = self.states[layer.id()][n]
                #set first column as checkbox
                item=QTableWidgetItem()
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if row[0]:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)
                item.setText("")
                table.setItem(n,0,item)
                #set second column as combobox
                combo = QComboBox();
                combo.addItems(row[1])
                #print (row[1],row[2])
                combo.setCurrentIndex(row[2])
                table.setCellWidget(n,1,combo)
                #set third column as attribute value
                item = QTableWidgetItem(row[3])
                item.setData(Qt.DisplayRole,row[4])
                if row[5]:
                    item.setForeground(QBrush(QColor(0,0,0)))
                else:
                    item.setForeground(QBrush(QColor(130,130,130)))
                if row[6]:
                    item.setBackground(QBrush(QColor(183,213,225)))
                table.setItem(n,2,item)

            table.blockSignals(False)
            return True

        else:
            return None



