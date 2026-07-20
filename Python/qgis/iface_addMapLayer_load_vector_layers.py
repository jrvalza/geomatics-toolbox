
#to view all data providers (ogr, gdal, etc)
#for prov in QgsProviderRegistry.instance().providerList():
#    print(prov)

#Load a shp with iface 
path1 = r'O:\xxxxxxx.shp'
iface.addVectorLayer(path1,'MUNICIPIOS','ogr')

#with addMapLayer (through the project)
path1 = r'O:\xxxxxxxx.shp'
capa = QgsVectorLayer(path1,'PROVINCIAS','ogr')
proyecto = QgsProject.instance()
proyecto.addMapLayer(capa)
