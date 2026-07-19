
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'

# List of fields
campos = [campo.name for campo in arcpy.ListFields(dataset='municipio.shp')]

# Adding a field 
if not 'DensiPOB95' in campos:
    arcpy.AddField_management(in_table='municipio.shp', 
                              field_name='DensiPOB95',
                              field_type= 'FLOAT', 
                              field_precision= 10, 
                              field_scale= 3)
    
# Update 'AREA_km2' field
with arcpy.da.UpdateCursor(in_table='municipio.shp', 
                           field_names=['POB95', 'SHAPE@AREA', 'DensiPOB95']) as uc:
    for fila in uc:
        fila[2] = float(fila[0]/(fila[1]/1000000))

        #update current row
        uc.updateRow(fila)

print('Proceso terminado.')

