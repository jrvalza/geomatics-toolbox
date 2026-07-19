
import os
import arcpy

arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

raster_path = os.path.join(arcpy.env.workspace, 'mde.tif')
if arcpy.CheckExtension('3D') == 'Available':
    arcpy.CheckOutExtension('3D')    

    arcpy.TinRaster_3d(in_tin='tin_64032',
                       out_raster=raster_path,
                       data_type='FLOAT',
                       method='LINEAR',
                       sample_distance='CELLSIZE 10',
                       z_factor=1
                       )#sample_distance can be either OBSERVATIONS or CELLSIZE
    
    arcpy.CheckInExtension('3D')
else:
    print("La extension 3D no esta disponible")

print("Grid creado")
