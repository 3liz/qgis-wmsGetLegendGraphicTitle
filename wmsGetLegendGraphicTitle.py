"""
***************************************************************************
    wmsGetLegendGraphicTitle.py
    ---------------------
    Date                 : October 2016
    Copyright            : (C) 2016 by René-Luc D'Hont - 3Liz
    Email                : rldhont at 3liz dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'DHONT René-Luc'
__date__ = 'October 2016'
__copyright__ = '(C) 2016-2019, DHONT René-Luc - 3Liz'

import traceback

from qgis.core import Qgis, QgsMessageLog
from qgis.server import QgsServerFilter
from qgis.PyQt.QtCore import QCoreApplication, QObject
from qgis.PyQt.QtWidgets import QAction, QMessageBox

import os.path

from xml.dom import minidom
from lxml import etree


class ServerGetLegendGraphicTitleFilter(QgsServerFilter):

    def requestReady(self) -> None:

        request = self.serverInterface().requestHandler()
        params  = request.parameterMap()

        if params.get('SERVICE', '').lower() == 'wms' \
            and params.get('REQUEST', '').lower() in ('getlegendgraphic','getlegendgraphics') \
            and not params.get('LAYERTITLE'):

            # get layers
            layers = params.get('LAYER') or params.get('LAYERS')
            # do something only we have one requested layer
            if layers:
                layers = layers.split(',')
                if len(layers) == 1:
                    layer = layers[0].strip()
                    # get QGIS project path
                    projectPath = self.serverInterface().configFilePath()
                    # read QGIS project to verify if layer is a map layer and not a group
                    if projectPath and os.path.exists( projectPath ):
                        request.setParameter('LAYERTITLE', 'FALSE')
                        tree = etree.parse(projectPath)
                        if tree.xpath("//layer-tree-group/customproperties/property[@key='wmsShortName'][@value='%s']" % layer):
                            request.setParameter('LAYERTITLE', 'TRUE')
                        elif tree.xpath("//layer-tree-group[@name='%s']" % layer):
                            request.setParameter('LAYERTITLE', 'TRUE')


class ServerGetLegendGraphicTitle:
    """Plugin for QGIS server"""

    def __init__(self, serverIface: 'QgsServerInterface') -> None:
        # Save reference to the QGIS server interface
        self.serverIface = serverIface
        self.serverIface.registerFilter(ServerGetLegendGraphicTitleFilter(serverIface), 1000)


class GetLegendGraphicTitle:

    def __init__(self, iface: 'QgsInterface') -> None:
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()

    def initGui(self) -> None:
        # Create action that will start plugin
        self.action = QAction(QIcon(":/plugins/"), "About Server GetLegendGraphicTitle", self.iface.mainWindow())
        # Add toolbar button and menu item
        self.iface.addPluginToMenu("Server GetLegendGraphicTitle", self.action)
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("activated()"), self.about)

    def unload(self) -> None:
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("Server GetLegendGraphicTitle", self.action)

    # run
    def about(self) -> None:
        QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('GetLegendGraphicTitle', "Server GetLegendGraphicTitle"), QCoreApplication.translate('GetFeatureInfoPrecision', "Server GetFeatureInfoPrecision is a simple plugin for QGIS Server, it does just nothing in QGIS Desktop. See: <a href=\"https://github.com/3liz/qgis-wmsGetLegendGraphicTitle\">plugin's homepage</a>"))


