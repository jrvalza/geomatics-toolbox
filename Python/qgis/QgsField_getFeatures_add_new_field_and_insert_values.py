
#============================================================================
#=========================add new field and insert values====================
#============================================================================
from math import sqrt

#project
proyecto = QgsProject.instance()

#Access the layer by name
capa = proyecto.mapLayersByName('PROVINCIA')[0] # returns a list with all layers or can be filtered by name
capa.removeSelection()

#===================================================
#==================Create new field=================
#===================================================
new_field = 'CC'

#fields names
campos = capa.fields() # QgsField object
 
#if field does not exist, we create it
if campos.indexFromName(new_field) == -1:
    #create
    nc = QgsField(name=new_field, type=QVariant.Double)
    
    #adding
    capa.dataProvider().addAttributes([nc])
    
    #update the field table
    capa.updateFields()


#===================================================
#==================insert values====================
#===================================================

#current field values
registros = capa.getFeatures()

#values in the CC field
for reg in registros:
    #get data
    attributes = reg.attribute(new_field) #access to the attribute
    geometry = reg.geometry() #access to the geometry
    
    #insert data
    id_reg = reg.id()
    id_field = reg.fieldNameIndex(new_field)
    cir_coef = 0.282 *(geometry.length()/ sqrt(geometry.area())) 
    data_update = {id_reg:{id_field:cir_coef}}
    
    #modify fields in the database
    capa.dataProvider().changeAttributeValues(data_update)
print("FIN")   
