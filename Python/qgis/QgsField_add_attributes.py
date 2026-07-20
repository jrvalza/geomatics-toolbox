
#============================================================================
#==============================Add new field=================================
#============================================================================

#project
proyecto = QgsProject.instance()

#Access to layer by name
capa = proyecto.mapLayersByName('PROVINCIA')[0] # returns a list with all layers or can be filtered by name
capa.removeSelection()

new_field = 'NC'

#fields names
campos = capa.fields() # QgsField object

#if the field does not exist, we create it
if campos.indexFromName(new_field) == -1:
    nc = QgsField(name=new_field, type=QVariant.Double)

#add the new field
capa.dataProvider().addAttributes([nc])

#update the layer
capa.updateFields()
   