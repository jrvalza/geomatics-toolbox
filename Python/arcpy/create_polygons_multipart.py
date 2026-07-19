
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'
arcpy.env.overwriteOutput = True

src = arcpy.SpatialReference(25830)
point1 = arcpy.Point(0, 0)
point2 = arcpy.Point(0, 100)
point3 = arcpy.Point(100, 100)
point4 = arcpy.Point(100, 0)
points1 = arcpy.Array([point1, point2, point3, point4, point1])
polygon1 = arcpy.Polygon(inputs=points1, spatial_reference=src)
print(f'Perimetro poligono 1: {polygon1.length}. Área poligono 1: {polygon1.area}')
#arcpy.Copy_management(polygons, 'polygons_agujero.shp')

point5 = arcpy.Point(200, 0)
point6 = arcpy.Point(200, 100)
point7 = arcpy.Point(300, 100)
point8 = arcpy.Point(300, 0)
points2 = arcpy.Array([[point1, point2, point3, point4, point1], [point5, point6, point7, point8, point5]])
polygon2 = arcpy.Polygon(inputs=points2, spatial_reference=src)
print(f'Perimetro poligono 2: {polygon2.length}. Área poligono 2: {polygon2.area}')
#arcpy.Copy_management(polygon2, 'polygons2.shp')

#Polygon with hole
point1 = arcpy.Point(0, 0)
point2 = arcpy.Point(0, 100)
point3 = arcpy.Point(100, 100)
point4 = arcpy.Point(100, 0)
point5 = arcpy.Point(25, 25)
point6 = arcpy.Point(25, 75)
point7 = arcpy.Point(75, 75)
point8 = arcpy.Point(75, 25)
point_hole = arcpy.Point()
points3= arcpy.Array([[point1, point2, point3, point4, point1, point_hole, point5, point6, point7, point8, point5]])
polygon3 = arcpy.Polygon(inputs=points3, spatial_reference=src)
print(f'Perimetro poligono 3: {polygon3.length}. Área poligono 3: {polygon3.area}')

polygons = [polygon1, polygon2, polygon3]
arcpy.CopyFeatures_management(polygons, 'polygons_agujero.shp')

print('Done')
