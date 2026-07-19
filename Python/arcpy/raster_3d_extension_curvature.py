
import os
import arcpy

arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

raster_path = os.path.join(arcpy.env.workspace, 'mde_curvature.tif')
if arcpy.CheckExtension('3D') == 'Available':
    arcpy.CheckOutExtension('3D')    

    arcpy.Curvature_3d(in_raster='mde.tif',
                       out_curvature_raster=raster_path,
                       z_factor=1
                       )
    arcpy.CheckInExtension('3D')
else:
    print("La extension 3D no esta disponible")

print("Curvature creado")