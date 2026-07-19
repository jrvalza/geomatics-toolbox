
import arcpy
import os

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxxxxx'
arcpy.env.overwriteOutput = True

out_folder = r'C:\xxxxxxxxxx'

#Buffer
buffer_path = os.path.join(out_folder, 'buf_1000.shp')
buf_1000 = arcpy.Buffer_analysis(in_features='nucleos.shp',
                                 out_feature_class=buffer_path,
                                 buffer_distance_or_field=1000,
                                 dissolve_option='All'
                                 )

#Clip using buffer
clip_path = os.path.join(out_folder, 'car_clip.shp')
car_clip = arcpy.Clip_analysis('carretera.shp',
                               clip_features=buf_1000,
                               out_feature_class=clip_path)

#Delete temp files
arcpy.Delete_management(in_data=buf_1000)

print('Proceso terminado')
