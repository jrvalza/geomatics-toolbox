
import os
import arcpy

arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

raster_path = os.path.join(arcpy.env.workspace, 'mde_slopes.tif')
if arcpy.CheckExtension('3D') == 'Available':
    arcpy.CheckOutExtension('3D')    

    arcpy.Slope_3d(in_raster='mde.tif',
                   out_raster=raster_path,
                   output_measurement='DEGREE', 
                   z_factor=1)
    
    arcpy.CheckInExtension('3D')
else:
    print("La extension 3D no esta disponible")

print("Slopes creado")