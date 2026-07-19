
import arcpy
import arcpy.mp as mp

#project
aprx = mp.ArcGISProject(r'C:\xxxxxxxxx.aprx')

#layouts
layout = aprx.listLayouts('plantilla1')[0]

#Mapframe
mf_detalle = layout.listElements('MAPFRAME_ELEMENT', 'Detalle')[0]

#camera
camara = mf_detalle.camera
camara.scale = 50000

#save project
aprx.save()

del aprx
