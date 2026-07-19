
import os
import arcpy
import numpy as np
from arcpy.sa import *

arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

#input data
mde_in = r'C:\xxxxxxxx\mde.tif'

def sombreados (mde, out_name, azimut, altitud):
    for i in range(len(out_name)):
        raster_path = os.path.join(arcpy.env.workspace, out_name[i])
        #Hillshade
        arcpy.HillShade_3d(in_raster = mde,
                           out_raster = raster_path,
                           azimuth = azimut[i],
                           altitude = altitud[i],
                           model_shadows = False,
                           z_factor = 1)
        
if arcpy.CheckExtension('3D') == 'Available':
    arcpy.CheckOutExtension('3D')    

    #Hillshades
    sombreados(mde=mde_in,
              out_name=['mde_sombreado1.tif','mde_sombreado2.tif'],
              azimut=[315, 225],
              altitud=[45, 45])
    
    #Map algebra
    hillshade_1 = arcpy.Raster('mde_sombreado1.tif')
    hillshade_2 = arcpy.Raster('mde_sombreado2.tif')
    hillshade_combinado = hillshade_1.getRasterInfo()
    hillshade_combinado = hillshade_1 + hillshade_2
    
    #desplazamiento y escalado de ND
    array_hill1 = arcpy.RasterToNumPyArray(hillshade_1)
    array_combinado = arcpy.RasterToNumPyArray(hillshade_combinado)

    # Rangos de entrada y salida
    Rs = np.max(array_hill1) - np.min(array_hill1)
    Re = np.max(array_combinado) - np.min(array_combinado)

    proportion = Rs/Re
    V = proportion * array_combinado

    #array to raste
    cell_size = hillshade_1.meanCellHeight
    frame = hillshade_1.extent
    x_min = frame.XMin
    y_min = frame.YMin
    lower_left_corner = arcpy.Point(x_min, y_min)
    new_raster = arcpy.NumPyArrayToRaster(in_array = V,
                                          lower_left_corner = lower_left_corner,
                                          x_cell_size = cell_size,
                                          y_cell_size = cell_size)

    #save new raster
    new_raster.save('hillshade_combinado.tif')

    arcpy.CheckInExtension('3D')

else:
    print("La extension 3D no esta disponible")

print("Finalizado")
