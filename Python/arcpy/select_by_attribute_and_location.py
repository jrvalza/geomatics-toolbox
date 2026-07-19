
"""
A script that selects the municipalities in Province X with more than 5,000 residents
that have train stations located within 40 kilometers of any reservoir.
"""

import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'
arcpy.env.overwriteOutput = True # to overwrite existing files and avoid errors

#Selections
sel1 = arcpy.SelectLayerByAttribute_management('municipio.shp', 'NEW_SELECTION', 'POB95>5000')
sel2 = arcpy.SelectLayerByLocation_management('estaciones.shp', 'WITHIN_A_DISTANCE', 'embalses.shp', 40000, 'NEW_SELECTION')
sel3 = arcpy.SelectLayerByLocation_management(sel1, 'INTERSECT', sel2, selection_type='SUBSET_SELECTION')

#Save information
arcpy.env.workspace = r'C:\xxxxxx'
arcpy.CopyFeatures_management(sel3, 'resultado_seleccion.shp')
print('proceso terminado.')
