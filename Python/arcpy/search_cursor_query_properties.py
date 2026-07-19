
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'

with arcpy.da.SearchCursor(in_table='provincia.shp', 
                           field_names=['NOMBRE', 'SHAPE@']) as cursor: #SHAPE@ allow to access the geometry directly
     for fila in cursor:
         nombre = fila[0]
         centroide = fila[1].centroid
         print(f'Nombre: {nombre}\n\tX centroide: {centroide.X}\n\tY centroide: {centroide.Y}')

print('Proceso terminado.')

