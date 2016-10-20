wmsGetLegendGraphicTitle: QGIS Server Plugin to remove layer title from GetLegendGraphic if one query layer.
=============================================================================================================

Description
---------------

wmsGetLegendGraphicTitle is a QGIS Server Plugin. It adds QGIS Server specific Layer Title parameter to false if :
* only one layer is requested
* the requested layer is not a groupe
* the request has not already LAYERTITLE parameter

Use it for a non QGIS Server specific client.