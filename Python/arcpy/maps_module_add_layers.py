
import sys
import arcpy
import arcpy.mp as mp #maps module

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

# Map Properties
print(f'Nombre: {mapa.name}')
print(f'Unidades de mapa: {mapa.mapUnits}')
print(f'Sistema de referencia: {mapa.spatialReference.name}')

#Add layer from path
shp_path = r'C:\xxxxxx.SHP'
mapa.addDataFromPath(shp_path)

#add base map
mapa.addBasemap('Calles')

#save project
aprx.save()

#delete project reference
del aprx
