
'''
Add vertices from CSV to shp file
'''

import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'

path = r'C:\xxxxxxx.csv'

# Data to insert
with open (path, 'r') as file:
    data = file.readlines()
    data_to_insert = []
    id = None
    x = None
    y = None
    for i in data:
        i = i.split(';')
        try:
            id = int(i[0])
            x = float(i[1])
            y = float(i[2])
            data_to_insert.append([id, (x,y)])
        except:
            pass

# Insert Cursor
with arcpy.da.InsertCursor(in_table='vertices.shp', 
                            field_names=['Id', 'SHAPE@XY']) as ic:
     for fila in data_to_insert:
         ic.insertRow(fila)

print('Proceso terminado.')

