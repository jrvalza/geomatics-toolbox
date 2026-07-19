
"""
Determine the area in hectares of forest that will be affected
by the 15-meter-wide expansion of the highway known as “Red C.O.P.U.T.”
"""

import arcpy
import os

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxxx'
arcpy.env.overwriteOutput = True

out_folder = r'C:\xxx'

#get road Red C.O.P.U.T
query = """ "TIPO" = 'Red C.O.P.U.T' """
comunic = arcpy.SelectLayerByAttribute_management('64032comunic.shp',
                                                 selection_type="NEW_SELECTION",
                                                 where_clause=query,
                                                 )

#get a bosque features
query = """ "TIPO" = 'Bosque' """
bosque = arcpy.SelectLayerByAttribute_management('64032cultivos.shp',
                                                 selection_type="NEW_SELECTION",
                                                 where_clause=query,
                                                 )

#Buffer
buffer_path = os.path.join(out_folder, 'buf_15.shp')
buf_15 = arcpy.Buffer_analysis(comunic,
                                 buffer_distance_or_field=100,
                                 dissolve_option='All',
                                 out_feature_class=buffer_path,
                                 )


#Clip using buffer
clip_path = os.path.join(out_folder, 'crop_clip.shp')
crop_clip = arcpy.Clip_analysis(bosque,
                               clip_features=buf_15,
                               out_feature_class=clip_path)

#compute area
with arcpy.da.SearchCursor(crop_clip, ['SHAPE@AREA']) as sc:
    area = 0
    for row in sc:
        area += row[0]

print(f"El area total afectada de bosque por ampliacion de 15 metros de las carreteras es de: {area/10000:.2f}ha")

print('Proceso terminado')
