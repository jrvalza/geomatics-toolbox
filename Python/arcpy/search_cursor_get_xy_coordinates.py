
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

with arcpy.da.SearchCursor(in_table='parques.shp', field_names=['NOMBRE', 'SHAPE@XY']) as sc:
    for fila in sc:
        print(f'Parque: {fila[0]}\n - XCoord: {fila[1][0]}\n - YCoord: {fila[1][1]} \n')

print('Proceso terminado.')

