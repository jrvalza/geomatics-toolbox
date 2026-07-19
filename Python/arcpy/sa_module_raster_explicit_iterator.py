
import arcpy
from arcpy.sa import *

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

#Rasters
raster = arcpy.Raster('mde1.asc')
raster_info = raster.getRasterInfo()
nuevo_raster = arcpy.Raster(raster_info)

#Kernel
filter_mean = [(-1, -1), (0, -1), (1, -1),
               (-1, 0), (0, 0), (1, 0),
               (-1, 1), (0, 1), (1, 1)
               ]

#Apply kernel to raster
with RasterCellIterator({'rasters':[raster, nuevo_raster]}) as rci:
    for fila, columna in rci:
        suma = 0
        for x, y in filter_mean:
            suma += raster[fila+x, columna+y] 
        media = suma / 9.0
        nuevo_raster[fila, columna] = media

#Save
nuevo_raster.save('elev_filtro_mean.tif')

print('Proceso terminado.')

