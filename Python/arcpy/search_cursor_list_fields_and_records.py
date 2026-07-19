
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

#fields (name and data type)
campos = arcpy.ListFields(dataset='provincia.shp')
cabecera = [campo.name for campo in campos if campo.type != 'Geometry']

print(cabecera)

# all records in dataset
with arcpy.da.SearchCursor(in_table='provincia.shp', field_names=cabecera) as sc:
    for fila in sc:
        print(list(fila))

print('Proceso terminado.')

