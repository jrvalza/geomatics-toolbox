
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'

#QUERY
query = 'POB95 > 50000'

with arcpy.da.SearchCursor(in_table='municipio.shp', field_names=['SHAPE@AREA'], where_clause=query) as sc:
    area = []
    for fila in sc:
        area.append(fila[0])
    print(f'Area media: {(sum(area)/len(area))/1000000:.3f} km2')

print('Proceso terminado.')

