
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'

#shp files in workspace
shp_list = arcpy.ListFeatureClasses()
for shp in shp_list:
    print(shp)

print('='*50)

#shp files in workspace that star with letter m
shp_list = arcpy.ListFeatureClasses('m*')
for shp in shp_list:
    print(shp)

print('='*50)

#shp files (polygon) in workspace
shp_list = arcpy.ListFeatureClasses(feature_type='Polygon')
for shp in shp_list:
    print(shp)
    