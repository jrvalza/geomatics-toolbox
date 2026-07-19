
import arcpy
import numpy as np

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

raster = arcpy.Raster('mde1.asc')

# raster to numpy
data = arcpy.RasterToNumPyArray(raster) # all data from raster file

print('Min: ', np.min(data))
print('Max: ', np.max(data))
print('Mean: ', np.mean(data))
print('STDV: ', np.std(data))

print('Proceso terminado.')

