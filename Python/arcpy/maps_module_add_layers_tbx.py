
import arcpy
import arcpy.mp as mp

#project
aprx = mp.ArcGISProject('CURRENT')

#map
map = aprx.listMaps('Detalle')[0]

#parameters
layer_path = arcpy.GetParameterAsText(index=0) #first parameter in the toolbox script

#add layer
map.addDataFromPath(layer_path)

#toolbox message
arcpy.AddMessage(f'Añadida la capa {layer_path}')
