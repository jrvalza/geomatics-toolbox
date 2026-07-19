
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

src = arcpy.Describe('municipio.shp').spatialReference

centroids = []
with arcpy.da.SearchCursor('municipio.shp', 'SHAPE@') as sc:
    for fila in sc:
        geom = fila[0] 
        centroid = geom.centroid
        point_geom = arcpy.PointGeometry(inputs=centroid,
                                         spatial_reference=src)
        centroids.append(point_geom)

#Output shp
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.CopyFeatures_management(centroids, 'Mun_centroids.shp')

print('Proceso terminado.')
