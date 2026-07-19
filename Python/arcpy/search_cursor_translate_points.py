
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

src = arcpy.Describe('municipio.shp').spatialReference
dx = 1000
dy = 1000
points = []

with arcpy.da.SearchCursor('estaciones.shp', 'SHAPE@') as sc:
    for fila in sc:
        geom = fila[0] 
        for point in geom:
             x = point.X + dx
             y = point.Y + dy 
             new_point = arcpy.PointGeometry(arcpy.Point(x,y), src)
             points.append(new_point)

#Output shp
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.CopyFeatures_management(points, 'Estaciones_desXY.shp')

print('Proceso terminado.')
