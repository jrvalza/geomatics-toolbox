
import arcpy
import numpy as np

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

raster = arcpy.Raster('mde1.asc')

cell_size =raster.meanCellHeight

# to georeferencing arrayToRaster
frame = raster.extent
x_min = frame.XMin
y_min = frame.YMin
lower_left_corner = arcpy.Point(x_min, y_min)

# raster to numpy
data = arcpy.RasterToNumPyArray(raster) # all data from raster file

#filter elevation
new_data = np.where(data >= 1000, 1, 0).astype(np.uint8) #result is 8 bits

#array to raster
new_raster = arcpy.NumPyArrayToRaster(in_array = new_data,
                                      lower_left_corner = lower_left_corner,
                                      x_cell_size = cell_size,
                                      y_cell_size = cell_size) #default cell size=1

#save new raster
new_raster.save('elev_1000_v3.tif')#without extension arcpy create a grid format

print('Proceso terminado.')
