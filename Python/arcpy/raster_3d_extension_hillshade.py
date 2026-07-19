
import os
import arcpy

arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

raster_path = os.path.join(arcpy.env.workspace, 'mde_sombreado.tif')
if arcpy.CheckExtension('3D') == 'Available':
    arcpy.CheckOutExtension('3D')    

    arcpy.HillShade_3d(in_raster='mde.tif',
                       out_raster=raster_path,
                       azimuth=315,
                       altitude=45,
                       model_shadows=False,
                       z_factor=1)
    
    arcpy.CheckInExtension('3D')
else:
    print("La extension 3D no esta disponible")

print("Hillshade creado")
