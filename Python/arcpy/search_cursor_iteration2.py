
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'
arcpy.env.overwriteOutput = True # to overwrite existing files and avoid errors

# Iteration with 'as' and a 'for' loop (RECOMMENDED)
with arcpy.da.SearchCursor('provincia.shp', ['NOMBRE']) as sc:
    for fila in sc:
        print(f'Nombre: {fila[0]}')

print('Proceso terminado.')

with arcpy.da.SearchCursor('provincia.shp', ['PROVI']) as sc:
    for fila in sc:
        print(f'Provi: {fila[0]}')

print('Proceso terminado.')
