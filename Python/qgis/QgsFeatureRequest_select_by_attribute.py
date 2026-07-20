
#select by SQL expression
#QgsFeatureRequest() -> for filtering 1-)expressions, 2-)rectangle or 3-)
#getFeatures ()

#project
proyecto = QgsProject.instance()

#Access to layer by name
capa = proyecto.mapLayersByName('PROVINCIA')[0] # returns a list with all layers or can be filtered by name
capa.removeSelection()

#all records
registros = capa.getFeatures()

#filter by SQL expression
query = """ NOMBRE = 'BURGOS' """
filtro = QgsFeatureRequest().setFilterExpression(query)
registros = capa.getFeatures(filtro)

ids=[i.id() for i in registros]
print("identificadores: ", ids)

#select by identifiers
capa.select(ids)

#then, zoom to the selection
marco = capa.boundingBoxOfSelected()
iface.mapCanvas().setExtent(marco) #Canvas extension
