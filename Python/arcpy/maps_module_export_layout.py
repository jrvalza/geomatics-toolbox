
import arcpy
import arcpy.mp as mp

#project
aprx = mp.ArcGISProject(r'C:\xxxxxxxxxxxxx.aprx')

#layouts
layout = aprx.listLayouts('plantilla1')[0]

#Mapframe
mf_detalle = layout.listElements('MAPFRAME_ELEMENT', 'Detalle')[0]

#camera
camara = mf_detalle.camera
camara.scale = 300000

#save project
layout.exportToPDF(r'C:\xxxxxxxx.pdf')

del aprx
