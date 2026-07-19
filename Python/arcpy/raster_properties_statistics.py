
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

raster = arcpy.Raster('30-S-YJ-2018-1-16-B11.tif')
print('Nombre: ',raster.name)
print('Path: ',raster.path)
print('SysRef: ',raster.spatialReference.name)
print('Formato: ',raster.format)
print('Nº bandas: ',raster.bandCount)
print('Tipo pixel: ',raster.pixelType)
print('Columnas: ',raster.width)
print('Filas: ',raster.height)
print('Tamaño de pixel: ',raster.meanCellWidth)

print('\nEstadisticas raster')
arcpy.CalculateStatistics_management(raster)
print('Valor mínimo: ',raster.minimum)
print('Valor máximo: ',raster.maximum)
print('Valor medio: ',raster.mean)
print('STDV: ',raster.standardDeviation)

print('Proceso terminado.')
