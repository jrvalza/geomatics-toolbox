
import arcpy

src = arcpy.SpatialReference(25830)
point1 = arcpy.Point(0, 0)
point2 = arcpy.Point(100, 100)
points = arcpy.Array([point1, point2])
polyline = arcpy.Polyline(inputs=points, spatial_reference=src)
print(f'Longitud linea 1: {polyline.length}\n')


point3 = arcpy.Point(0, 100)
point4 = arcpy.Point(100, 0)
points = arcpy.Array([point3])
points.append(point4)
polyline2 = arcpy.Polyline(inputs=points, spatial_reference=src)

geom_intersect = polyline.intersect(other=polyline2, dimension=1) # output: PointGeometry
pto_intersect = geom_intersect.firstPoint
print(geom_intersect[0])
print(f'Intersección linea 1 y linea 2: x={pto_intersect.X} Y={pto_intersect.Y}') 
