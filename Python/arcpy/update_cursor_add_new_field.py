
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'

# List of fields
campos = [campo.name for campo in arcpy.ListFields(dataset='municipio.shp')]

# Adding a field 
if not 'AREA_km2' in campos:
    arcpy.AddField_management(in_table='municipio.shp', 
                              field_name='AREA_km2',
                              field_type= 'FLOAT', 
                              field_precision= 10, 
                              field_scale= 3)# decimals
    
# Update 'AREA_km2' field
with arcpy.da.UpdateCursor(in_table='municipio.shp', 
                           field_names=['SHAPE@AREA', 'AREA_km2']) as uc:
    for fila in uc:
        fila[1] = float(fila[0]/1000000)

        #update current row
        uc.updateRow(fila)

print('Proceso terminado.')

