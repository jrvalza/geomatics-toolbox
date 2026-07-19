
import arcpy

arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

#Eit TIN
path_cotas = r"C:\xxxxxxx\puntos_cota.shp"
path_cn = r"C:\xxxxxxx\curvas_nivel.shp"
path_bl = r"C:\xxxxxxx\hidrog_lin.shp"

#Plantilla para uso de licencias en ArcGIS
if arcpy.CheckExtension('3D') == 'Available':
    arcpy.CheckOutExtension('3D')

    #EmptyTIN
    arcpy.CreateTin_3d('tin_64032')

    #EdiTIN
    entities = [[path_cotas, 'COTA', '<None>', 'masspoints', False],
                [path_cn, 'COTA', '<None>', 'softline', False],
                [path_bl, '<None>', '<None>', 'hardline', True]] 
    arcpy.EditTin_3d('tin_64032', entities, True)

    #Raster MDE
    raster_path = os.path.join(arcpy.env.workspace, 'mde.tif')
    arcpy.TinRaster_3d(in_tin='tin_64032',
                       out_raster=raster_path,
                       data_type='FLOAT',
                       method='LINEAR',
                       sample_distance='CELLSIZE 10',
                       z_factor=1
                       )#sample_distance can be either OBSERVATIONS or CELLSIZE
    
    #Raster Hillshade
    raster_path = os.path.join(arcpy.env.workspace, 'hillshade.tif')
    arcpy.HillShade_3d(in_raster='mde.tif',
                       out_raster=raster_path,
                       azimuth=315,
                       altitude=45,
                       model_shadows=False,
                       z_factor=1)
    
    #Raster slopes
    raster_path = os.path.join(arcpy.env.workspace, 'Slopes.tif')   
    arcpy.Slope_3d(in_raster='mde.tif',
                   out_raster=raster_path,
                   output_measurement='DEGREE', 
                   z_factor=1)
    
    #Raster aspect
    raster_path = os.path.join(arcpy.env.workspace, 'mde_aspect.tif')
    arcpy.Aspect_3d(in_raster='mde.tif',
                    out_raster=raster_path,
                    method='PLANAR',
                    z_unit='METER')
    
    #Raster curvature
    raster_path = os.path.join(arcpy.env.workspace, 'mde_curvature.tif')
    arcpy.Curvature_3d(in_raster='mde.tif',
                       out_curvature_raster=raster_path,
                       z_factor=1
                       )

    arcpy.CheckInExtension('3D')
else:
    print("La extension 3D no esta disponible")

print("Fin del proceso")   
