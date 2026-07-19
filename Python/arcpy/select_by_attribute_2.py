
import os
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True 

#query
query = ''' "CODPROV" = '24' '''
selection = arcpy.SelectLayerByAttribute_management('municipio.shp', selection_type='NEW_SELECTION', where_clause=query)

#Number of selected elements
nsel = arcpy.GetCount_management(selection)
print(f'Municipios con codigo de provincia 24:{nsel}')

#save selection
salida = r'C:\xxxxxx'
arcpy.CopyFeatures_management(selection, os.path.join(salida,'mun_codprov_24.shp'))

