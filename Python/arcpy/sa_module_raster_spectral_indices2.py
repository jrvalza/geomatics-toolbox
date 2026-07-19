
'''
Calculating a NDVI index from a Landsat 8 image
'''

import arcpy
import numpy as np
from arcpy.sa import *
from matplotlib import pyplot as plt

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'
arcpy.env.overwriteOutput = True

'''
NDVI = (NIR-R)/(NIR+R)
NIR = B5
R = B4
'''
#Rasters

R = arcpy.Raster('2018-08-25-LC08-200032-20180825-B4.tif')
NIR = arcpy.Raster('2018-08-25-LC08-200032-20180825-B5.tif')
ndvi = R.getRasterInfo()

#Map algebra
ndvi = (NIR-R) / (NIR+R)
ndvi.save('L8_NDVI.tif')

#Check output
ndvi_array = arcpy.RasterToNumPyArray(ndvi)
print('Mean: ', np.mean(ndvi_array))
print('Min: ', np.min(ndvi_array))
print('Max: ', np.max(ndvi_array))

#Draw Image
def draw_images(img):
    fig, aux = plt.subplots(1, 2)
    aux[0].imshow(img[0][0], cmap='gray')
    aux[0].set_title(img[0][1])

    aux[1].imshow(img[1][0], cmap='gray')
    aux[1].set_title(img[1][1])

    plt.show()

#output
NIR_array = arcpy.RasterToNumPyArray(NIR)
    
#Matplotlib
draw_image = [[NIR_array, 'NIR Band'], [ndvi_array, 'NDVI Index']]
draw_images(draw_image)

print('Proceso terminado.')

