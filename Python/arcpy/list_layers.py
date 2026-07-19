
import sys
import arcpy
import arcpy.mp as mp

aprx_path = r'C:\xxxxxx.aprx'

#Check path
if not arcpy.Exists(aprx_path):
    print('Path not valid')
    sys.exit()

#project reference
aprx = mp.ArcGISProject(aprx_path)

#list of maps in project
mapa = aprx.listMaps()[0] #list of maps
                       #listMaps(wildcard) wildcard: pattern of search

#list of layers
layers = mapa.listLayers()
for layer in layers:
    if layer.isFeatureLayer:
        print(f'Name: {layer.name}')
        print(f'Type: vectorial\n')
    
    if layer.isRasterLayer:
        print(f'Name: {layer.name}')
        print(f'Type: raster\n')
    
    if layer.isBasemapLayer:
        print(f'Name: {layer.name}')
        print(f'Type: Base map\n')
    

#delete project reference
del aprx

