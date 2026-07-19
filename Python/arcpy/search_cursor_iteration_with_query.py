
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'
arcpy.env.overwriteOutput = True

#QUERY
query = 'POB95 > 50000'

with arcpy.da.SearchCursor(in_table='municipio.shp', field_names=['NOMBRE', 'POB95', 'SHAPE@AREA'], where_clause=query) as sc:
    for fila in sc:
        print(f'Nombre: {fila[0]}\n - POB95: {fila[1]}\n - AREA: {fila[2]/1000000:.2f} km^2\n')

print('Proceso terminado.')

