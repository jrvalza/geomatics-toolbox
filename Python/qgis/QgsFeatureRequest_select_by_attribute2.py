
#project
proyecto = QgsProject.instance()

#Access to layer by name
capa = proyecto.mapLayersByName('MUNICIPIO')[0]
capa.removeSelection()

#all records
registros = capa.getFeatures()

#filter by SQL expression
query = 'POB95 > 50000'
filtro = QgsFeatureRequest().setFilterExpression(query)
registros = capa.getFeatures(filtro)

ids=[i.id() for i in registros]
print("identificadores: ", ids)

#select by identifiers
capa.select(ids)

#zoom to the selection
marco = capa.boundingBoxOfSelected()
iface.mapCanvas().setExtent(marco) #Canvas extension
