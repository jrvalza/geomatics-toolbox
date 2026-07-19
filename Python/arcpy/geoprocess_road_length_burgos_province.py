
import arcpy
import os

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxxx'
arcpy.env.overwriteOutput = True

out_folder = r'C:\xxxxxxxx'

#get a burgos province
query = """ "NOMBRE" = 'BURGOS' """
burgos = arcpy.SelectLayerByAttribute_management('provincia.shp',
                                                 selection_type="NEW_SELECTION",
                                                 where_clause=query
                                                 )

#Clip using provincia selection
clip_path = os.path.join(out_folder, 'car_clip_burgos.shp')
car_clip_burgos = arcpy.Clip_analysis('carretera.shp',
                               clip_features=burgos,
                               out_feature_class=clip_path)

#compute len
with arcpy.da.SearchCursor(car_clip_burgos, ['SHAPE@LENGTH']) as sc:
    long = 0
    for row in sc:
        long += row[0]

print(f"Longitud total de carreteras en la provincia de Burgos es: {long/1000:.2f}km")

print('Proceso terminado')
