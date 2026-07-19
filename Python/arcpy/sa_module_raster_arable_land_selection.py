
'''
Select the arable land based on two criteria:
1-) slope < 10% 
2-) 1000 <= elevation <= 1200
'''

import arcpy
from arcpy.sa import *

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

#Raster
mde = arcpy.Raster('mde2.asc')

#Extension checking
if arcpy.CheckExtension('Spatial') == 'Available':
    arcpy.CheckOutExtension('Spatial')    
    
    #slope map
    slope = Slope(in_raster=mde,
                  output_measurement='PERCENT_RISE')
    #criteria 1
    slope_down = slope <= 10 #create  a binary map

    #criteria 2
    altitud = (mde >= 1000)  & (mde <= 1200)

    #Result
    crops = slope_down & altitud
    crops.save('cultivos.tif')
    arcpy.CheckInExtension('Spatial') #leave the license

else:
    print('Licencing not available')

print('Proceso terminado.')
