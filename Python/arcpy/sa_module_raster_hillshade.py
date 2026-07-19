
import arcpy
from arcpy.sa import *

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

#Raster
mde = arcpy.Raster('mde1.asc')

#Extension checking
if arcpy.CheckExtension('Spatial') == 'Available':
    arcpy.CheckOutExtension('Spatial')    
    
    #hillshade
    hillshade = Hillshade(in_raster=mde,
                          azimuth = 315,
                          altitude = 45)
    hillshade.save('hs_mde1.tif')
    arcpy.CheckInExtension('Spatial') #leave the license

else:
    print('Licencing not available')

print('Proceso terminado.')
