
proyecto = QgsProject.instance()

#Access to layer by name
capa = proyecto.mapLayersByName('ESTACIONES')[0]

#create a spatial index
indice = QgsSpatialIndex()

#Add features to the index
for feat in capa.getFeatures():
    indice.insertFeature(feat)

nv = 5 #number of neighbors

#search for the 5 nearest neighbors (IDs)
vecinos = indice.nearestNeighbor(QgsPointXY(260806,4637930),nv)
capa.select(vecinos) #selection on screen

#Access to the features based on their IDs
request = QgsFeatureRequest().setFilterFids(vecinos) 
lista_entidades = [feat for feat in capa.getFeatures(request)]

for entidad in lista_entidades:
    print (entidad.attribute("FERROCA_ID"))
