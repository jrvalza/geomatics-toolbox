
import arcpy
import arcpy.mp as mp

aprx = mp.ArcGISProject('CURRENT')

#Interface comunication
estado = arcpy.GetParameter(0) #boolean parameter
mapa = aprx.listMaps()[0] # map acces
capas = mapa.listLayers() # layer access
 
for capa in capas:
    if capa.visible is True:
        capa.visible = False
    else:
        capa.visible = True

