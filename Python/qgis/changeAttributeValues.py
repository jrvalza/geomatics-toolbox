
#============================================================================
#======================modification of attributes============================
#============================================================================
#capa.dataProvider().changeAttributeValues({'id':{'campo':valor}})
#                                            id=reg.id()
#                                            campo = reg.fieldNameIndex('NOMBRE')
#                                            valor = el que se quiera insertar

#project
proyecto = QgsProject.instance()

#Access to layer by name
capa = proyecto.mapLayersByName('PROVINCIA')[0]
capa.removeSelection()

#values of the fields
registros = capa.getFeatures()

#values in the FID, 'NOMBRE' and GEOMETRY fields
field = 'NOMBRE'
for reg in registros:
    if 'VALLADOLID' in reg.attribute(field):
        
        id_reg = reg.id()
        id_field = reg.fieldNameIndex(field)
        value = 'VALLADOLID'
        
        data_update = {id_reg:{id_field:value}}

        #modify the values in the database
        capa.dataProvider().changeAttributeValues(data_update)
        print("FIN")
        