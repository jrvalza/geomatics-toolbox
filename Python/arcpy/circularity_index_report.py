
"""
Calculating the polygon circularity index using arcpy.da and geometry tokens, with generation of a text report
"""

import arcpy
from math import pi

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'
layer = 'provincia.shp'

# List of fields
campos = [campo.name for campo in arcpy.ListFields(dataset= layer)]

# Adding a field 
if not 'Coef_Cir' in campos:
    arcpy.AddField_management(in_table= layer, 
                              field_name='Coef_Cir',
                              field_type= 'FLOAT', 
                              field_precision= 10, 
                              field_scale= 2)# field_scale = number of decimales
    
# Update 'Coef_Cir' field
with arcpy.da.UpdateCursor(in_table=layer, 
                           field_names=['SHAPE@LENGTH', 'SHAPE@AREA', 'Coef_Cir']) as uc:
    for fila in uc:
        fila[2] = float((4*pi*fila[1])/(fila[0]**2))

        #update current row
        uc.updateRow(fila)

# Layer data
def layer_data (workspace, layer_shp):
    desc = arcpy.da.Describe(workspace +'\\'+ layer_shp)
    baseName_extension= desc['baseName'] +'.'+ desc['extension']
    catalogPath = desc['catalogPath'] 
    return (baseName_extension, catalogPath)

# File txt
with open (r'C:\xxxxxx.txt', 'w') as txt:
    txt.write('ANALISIS DEL COEFICIENTE DE CIRCULARIDAD\n'+ '*'*60 +'\n'*2)
    
    txt.write('DATOS DE LA CAPA\n'+ '-'*60 +'\n')
    layerData = layer_data(arcpy.env.workspace, layer)
    txt.write(f'NOMBRE:\t {layerData[0]}\n')
    txt.write(f'RUTA:\t {layerData[1]}'+ '\n'*2)
    
    # SearchCursor
    txt.write('RESULTADO\n'+ '-'*60 +'\n')
    txt.write(f'NOMBRE \t\t AREA(km2) \t PERIMETRO(km) \t CIRCULARIDAD\n')
    
    with arcpy.da.SearchCursor(in_table=layer, field_names=['NOMBRE', 'SHAPE@AREA', 'SHAPE@LENGTH', 'Coef_Cir']) as sc:
        area = []
        perimetro = []
        circularidad = []

        for line in sc:
            area.append(line[1])
            perimetro.append(line[2])
            circularidad.append(line[3])
            txt.write(f'{line[0]:<10} \t {round(line[1]/1000000,2)} \t {round(line[2]/1000,2)} \t {round(line[3],2)}\n')
        
        txt.write('\n'*2 +'RESUMEN\n'+ '-'*60 +'\n')
        txt.write(f'AREA MEDIA: {round((sum(area)/len(area))/1000000,2)} km2\n')
        txt.write(f'PERIMETRO MEDIO: {round((sum(perimetro)/1000)/len(perimetro),2)} km\n')
        txt.write(f'CIRCULARIDAD MEDIA: {round(sum(circularidad)/len(circularidad),2)}')

    txt.close()

print('Proceso terminado.')

