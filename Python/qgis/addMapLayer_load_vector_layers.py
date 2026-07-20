
proyecto = QgsProject.instance()

#with addMapLayer (through the project)
path1 = r'O:\xxxxxx.shp'
capa = QgsVectorLayer(path1,'NUCLEOS','ogr')

if capa.isValid():    
    proyecto.addMapLayer(capa)
else:
    print('Error al cargar la capa')
