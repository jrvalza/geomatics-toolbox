
"""
Calculation of a spectral index and a binary mask from a satellite image
"""

import arcpy
from arcpy.sa import *
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

#workspace definition
arcpy.env.workspace = r'C:\Projects\xxxxxx'
arcpy.env.overwriteOutput = True

#Upload Images as Rasters object arcpy
rgb = mpimg.imread(r'C:\datasets\LC09_L1TP_198033_20230105_20230314_02_T1.jpg')
b3 = arcpy.Raster('LC09_L1TP_198033_20230105_20230314_02_T1_B3.tif')
b5 = arcpy.Raster('LC09_L1TP_198033_20230105_20230314_02_T1_B5.tif')

#Map algebra to compte NDWI index and save file
ndwi = b3.getRasterInfo() #copy metadata from b3 band
ndwi = (b3-b5) / (b3+b5) # map algebra
ndwi.save('L9_NDWI_Index.tif')

#Save NDWI mask and convert to a numpy array
ndwi_mask = ndwi>0 #binary map. 1 for water areas and 0 for not water areas
ndwi_mask.save('NDWI_mask.tif')
mask=arcpy.RasterToNumPyArray(ndwi_mask,).astype()

#Draw Image
def draw_images(img):
    fig, aux = plt.subplots(1, 2)
    aux[0].imshow(img[0][0])
    aux[0].set_title(img[0][1])

    aux[1].imshow(img[1][0], cmap='gray')
    aux[1].set_title(img[1][1])

    plt.show()

#output Matplotlib visualizaccerfef
draw_image = [[rgb, 'RGB L9 image'], [mask, 'NDWI Index mask']]
draw_images(draw_image)

print('Proceso terminado.')

