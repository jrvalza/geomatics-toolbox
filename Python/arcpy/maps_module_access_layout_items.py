
import arcpy
import arcpy.mp as mp

#project
aprx = mp.ArcGISProject(r'C:\xxxxxxxxx.aprx')

#layouts
layout = aprx.listLayouts('plantilla1')[0]

#layout elements
for element in layout.listElements():
    print(element.type)

for elemnt in layout.listElements('TEXT_ELEMENT'):
    print(f'Tipo: {elemnt.type} - Nombre: {elemnt.name} - Texto: {elemnt.text}\nX(papel): {elemnt.elementPositionX} - Y(papel): {elemnt.elementPositionY}')
