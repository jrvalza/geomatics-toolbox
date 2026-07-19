
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'
arcpy.env.overwriteOutput = True # to overwrite existing files and avoid errors


# List of fields
campos = [campo.name for campo in arcpy.ListFields(dataset='vertices.shp')]

# Data to insert
new_data = [(1, (348000, 4620000)),
         (2, (482500, 4605000))]

# Insert Cursor
with arcpy.da.InsertCursor(in_table='vertices.shp', 
                            field_names=['Id', 'SHAPE@XY']) as ic:
     for fila in new_data:
         ic.insertRow(fila)

print('Proceso terminado.')

