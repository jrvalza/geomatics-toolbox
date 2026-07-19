
"""
Split the layer into individual layers based on the unique values of an attribute
"""

import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'
arcpy.env.overwriteOutput = True # to overwrite existing files and avoid errors

lista_nombres = ['BURGOS', 'LEON', 'ZAMORA', 'AVILA', 'SEGOVIA', 'SALAMANCA', 'VALLADOLID1', 'PALENCIA', 'SORIA']

dir_salida = r'C:\xxxxxx'

for nombre in lista_nombres:
    consulta = '"NOMBRE"= ' + "'" +nombre+ "'"
    print(consulta)
    sel = arcpy.SelectLayerByAttribute_management('provincia.shp', 'NEW_SELECTION', consulta)
    arcpy.CopyFeatures_management(sel, dir_salida+'\\'+nombre+'.shp')

print('Proceso terminado.')
