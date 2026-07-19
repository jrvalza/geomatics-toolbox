
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

buffers = []
with arcpy.da.SearchCursor('Autovia_A3.shp', 'SHAPE@') as sc:
    for fila in sc:
        geom = fila[0] 
        buffer = geom.buffer(500)
        buffers.append(buffer)

#Output shp
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.CopyFeatures_management(buffers, 'A3_Buffer.shp')

print('Proceso terminado.')

