# -*- coding: utf-8 -*-
"""
 This script initializes the plugin, making it known to QGIS.
"""


def serverClassFactory(serverIface):
    from wmsGetLegendGraphicTitle import ServerGetLegendGraphicTitle
    return ServerGetLegendGraphicTitle(serverIface)

def classFactory(iface):
    from wmsGetLegendGraphicTitle import GetLegendGraphicTitle
    return GetLegendGraphicTitle(iface)

