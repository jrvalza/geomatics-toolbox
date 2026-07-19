
import os
import arcpy

arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

raster_path = os.path.join(arcpy.env.workspace, 'mde_aspect.tif')
if arcpy.CheckExtension('3D') == 'Available':
    arcpy.CheckOutExtension('3D')    

    arcpy.Aspect_3d(in_raster='mde.tif',
                    out_raster=raster_path,
                    method='PLANAR',
                    z_unit='METER')
    
    arcpy.CheckInExtension('3D')
else:
    print("La extension 3D no esta disponible")

print("Aspect creado")
