
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

raster = arcpy.Raster('30-S-YJ-2018-1-16-B11.tif')

# Access to the pixel values
filas = raster.height
columnas = raster.width

# doble loop
for fila in range (0, filas):
    for columna in range (0, columnas):
        valor = raster[fila, columna]
        print(fila, columna, valor)
        break
    break

#one loop
for fila, columna in raster:
    print(fila, columna, raster[fila, columna])
    break

print('Proceso terminado.')
