
import sys
import arcpy
import arcpy.mp as mp

#======================================================
#==================Script for toolbox==================
#======================================================
''' THE ROUTE IS CHANGED TO THE current'''
aprx_path = r'CURRENT'

#Check path
'''if not arcpy.Exists(aprx_path):
    print('Path not valid')
    sys.exit()
'''
#project reference
aprx = mp.ArcGISProject(aprx_path)

#list of maps in project
mapa = aprx.listMaps()[0] #list of maps
                       #listMaps(wildcard) wildcard: pattern of search

#list of layers
layers = mapa.listLayers()
for layer in layers:
    if layer.isFeatureLayer:
        ''' The prints are replaced with arcpy.AddMessage'''
        arcpy.AddMessage(f'Name: {layer.name} - Type: vectorial\n')
    
    if layer.isRasterLayer:
        arcpy.AddMessage(f'Name: {layer.name} - Type: raster\n')
    
    if layer.isBasemapLayer:
        arcpy.AddMessage(f'Name: {layer.name} - Type: Base map\n')
    
#delete project reference
del aprx

