wmsGetLegendGraphicTitle: QGIS Server Plugin to remove layer title from GetLegendGraphic if one query layer.
=============================================================================================================

Description
---------------

wmsGetLegendGraphicTitle is a QGIS Server Plugin. It adds QGIS Server specific Layer Title parameter to false if :

* Only one layer is requested
* The requested layer is not a group
* The request does not have a LAYERTITLE parameter

Use it for a non QGIS Server specific client.

Needs *lxml* python module.

