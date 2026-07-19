
import arcpy.da as da

shp_path = r'C:\xxxxxxx.shp'

desc = da.Describe(shp_path)

print(f"path: {desc['catalogPath']}")

print(f"Base name: {desc['baseName']}")
print(f"Type of data: {desc['dataType']}")
print(f"Geometry type: {desc['shapeType']}")
print(f"Spatial reference: {desc['spatialReference'].name}")

marco = desc['extent']
print(f"Xmin: {marco.XMin} - Xmax: {marco.XMax} - Ymin: {marco.YMin} - Ymax: {marco.YMax}")

