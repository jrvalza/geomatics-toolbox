
#mapLayers() returns a dictionary
#mapLayersByName() returns a list

#Access to the QGIS project
pro = QgsProject.instance()

#layer of the project through mapLayers()
capas = pro.mapLayers()
for capa in capas.values():
    print(capa.name())
    
print("*"*10)

#layer of the project through mapLayersByName()
capa_sel = pro.mapLayersByName('MUNICIPIO')[0]
print(capa_sel.name())
