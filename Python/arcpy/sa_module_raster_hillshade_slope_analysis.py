
import arcpy
from arcpy.sa import *
from matplotlib import pyplot as plt

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

#Raster
mde = arcpy.Raster('mde2.asc')

def draw_images(img):
    fig, aux = plt.subplots(1, 3)
    aux[0].imshow(img[0][0], cmap='gray')
    aux[0].set_title(img[0][1])

    aux[1].imshow(img[1][0], cmap='gray')
    aux[1].set_title(img[1][1])

    aux[2].imshow(img[2][0], cmap='gray')
    aux[2].set_title(img[2][1])  

    plt.show()  

#Extension checking
if arcpy.CheckExtension('Spatial') == 'Available':
    arcpy.CheckOutExtension('Spatial')    
    
    #slope map
    slope = Slope(in_raster=mde,
                  output_measurement='PERCENT_RISE')
    #criteria 1
    hs1 = Hillshade(mde, 315, 45)
    hs2 = Hillshade(mde, 45, 30)
    arcpy.CheckInExtension('Spatial') #leave the license

    # raster to numpy
    hs1_array = arcpy.RasterToNumPyArray(hs1) # all data from raster file
    hs2_array = arcpy.RasterToNumPyArray(hs2)
    mde_array = arcpy.RasterToNumPyArray(mde)

    #Matplotlib
    draw_image = [[mde_array, 'MDE'], [hs1_array, 'A=315 E=45'], [hs2_array, 'A=45 E=30']]
    draw_images(draw_image)


else:
    print('Licencing not available')


print('Proceso terminado.')
