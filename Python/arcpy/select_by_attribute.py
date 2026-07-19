
import os
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'
arcpy.env.overwriteOutput = True

#query
query = '"POB95" > 50000'
selection = arcpy.SelectLayerByAttribute_management('municipio.shp', selection_type='NEW_SELECTION', where_clause=query)

#Number of selected elements
nsel = arcpy.GetCount_management(selection)
print(f'Municipios con más de 5000 habitantes:{nsel}')

#save selection
salida = r'C:\xxxxxx'
arcpy.CopyFeatures_management(selection, os.path.join(salida,'mun_pob95_50000.shp'))

