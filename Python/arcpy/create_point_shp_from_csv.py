
"""
Creating a point SHP file without having to create a layer first.
The layer is created based solely on the geometry. The layer attributes should be created or updated afterward.
"""
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'
arcpy.env.overwriteOutput = True

#Init
src = arcpy.SpatialReference(25830)
geometrias = []
path_csv = r'C:\xxxxxx.csv'

#Read CSV file and conversion type data (Point to PointGeometry) with src
with open (path_csv, 'r') as file:
    data = file.readlines()
    id = None
    x = None
    y = None
    for i in data:
        i = i.split(';')
        try:
            x = float(i[1])
            y = float(i[2])
            punto = arcpy.Point(x,y)
            punto_geom = arcpy.PointGeometry(punto, src)
            geometrias.append(punto_geom)
        except:
            pass

#Output shp
arcpy.CopyFeatures_management(geometrias, 'puntos.shp')
print('Proceso terminado.')

