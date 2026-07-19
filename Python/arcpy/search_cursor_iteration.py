
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'

#Iteration using only a for loop (NOT RECOMMENDED)
# sc = arcpy.da.SearchCursor('provincia.shp', ['NOMBRE'])
# for fila in sc:
#     print(fila[0])

# Iterating with 'as' and a 'for' loop (RECOMMENDED)
with arcpy.da.SearchCursor('provincia.shp', ['NOMBRE', 'PROVI']) as sc:
    for fila in sc:
        print(f'Nombre: {fila[0]} Provi: {fila[1]}')

print('Proceso terminado.')
