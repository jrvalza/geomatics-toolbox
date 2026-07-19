
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

raster = arcpy.Raster('mde1.asc')

#Copy metadata 
raster_info = raster.getRasterInfo() #access to template of properties raster

#Set pixel type to metadata copy
raster_info.setPixelType('S8') #integer 8 bits [0, 255] ND
print(raster_info.getPixelType())

#Create new raster 
mapa_binario = arcpy.Raster(raster_info)
for f, c in raster:
    if raster[f,c] >= 1000 and raster[f,c] <= 1500:
        mapa_binario[f,c]=1
    else:
        mapa_binario[f,c]=0

#save new raster
mapa_binario.save('elev_1000_1500.tif')#without extension arcpy create a grid format

print('Proceso terminado.')
