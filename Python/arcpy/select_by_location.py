
import os
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'
arcpy.env.overwriteOutput = True

#Selection
selection = arcpy.SelectLayerByLocation_management('municipio.shp', 
                                                   overlap_type='INTERSECT', 
                                                   select_features='estaciones.shp')

#Number of selected elements
nsel = arcpy.GetCount_management(selection)
print(f'Municipios con estaciones de ferrocarril:{nsel}')

#save selection
salida = r'C:\xxxxxx'
arcpy.CopyFeatures_management(selection, os.path.join(salida,'mun_estaciones.shp'))
