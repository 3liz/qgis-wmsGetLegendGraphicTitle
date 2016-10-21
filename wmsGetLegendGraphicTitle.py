# -*- coding: utf-8 -*-

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
__copyright__ = '(C) 2016, DHONT René-Luc - 3Liz'

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.server import *

import os.path
from xml.dom import minidom
from lxml import etree

class ServerGetLegendGraphicTitleFilter(QgsServerFilter):

    def requestReady(self):
        request = self.serverInterface().requestHandler()
        params = request.parameterMap( )
        if params.get('SERVICE', '').lower() == 'wms' \
            and params.get('REQUEST', '').lower() in ('getlegendgraphic','getlegendgraphics') \
            and not params.get('LAYERTITLE',''):
            # get layers
            layers = params.get('LAYER','')
            if not layers:
                layers = params.get('LAYERS','')
            # do something only we have one requested layer
            if layers and len(layers.split(',')) == 1 and layers.split(',')[0]:
                layer = layers.split(',')[0].strip()
                # get QGIS project path
                projectPath = os.getenv("QGIS_PROJECT_FILE")
                if not projectPath and 'map' in params :
                    projectPath = params['map']
                elif not projectPath and 'MAP' in params :
                    projectPath = params['MAP']
                # read QGIS project to verify if layer is a map layer and not a group
                if projectPath and os.path.exists( projectPath ) :
                    request.setParameter('LAYERTITLE', 'FALSE')
                    tree = etree.parse(projectPath)
                    if tree.xpath("//layer-tree-group/customproperties/property[@key='wmsShortName'][@value='%s']" % layer):
                        request.setParameter('LAYERTITLE', 'TRUE')
                    elif tree.xpath("//layer-tree-group[@name='%s']" % layer):
                        request.setParameter('LAYERTITLE', 'TRUE')


class ServerGetLegendGraphicTitle:
    """Plugin for QGIS server"""

    def __init__(self, serverIface):
        # Save reference to the QGIS server interface
        self.serverIface = serverIface
        try:
            self.serverIface.registerFilter(ServerGetLegendGraphicTitleFilter(serverIface), 1000)
        except Exception, e:
            QgsLogger.debug("ServerGetLegendGraphicTitle- Error loading filter %s", e)



class GetLegendGraphicTitle:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()


    def initGui(self):
        # Create action that will start plugin
        self.action = QAction(QIcon(":/plugins/"), "About Server GetLegendGraphicTitle", self.iface.mainWindow())
        # Add toolbar button and menu item
        self.iface.addPluginToMenu("Server GetLegendGraphicTitle", self.action)
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("activated()"), self.about)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("Server GetLegendGraphicTitle", self.action)

    # run
    def about(self):
        QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('GetLegendGraphicTitle', "Server GetLegendGraphicTitle"), QCoreApplication.translate('GetFeatureInfoPrecision', "Server GetFeatureInfoPrecision is a simple plugin for QGIS Server, it does just nothing in QGIS Desktop. See: <a href=\"https://github.com/3liz/qgis-wmsGetLegendGraphicTitle\">plugin's homepage</a>"))



if __name__ == "__main__":
    pass
