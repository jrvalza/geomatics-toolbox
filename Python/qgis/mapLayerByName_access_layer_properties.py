
proyecto = QgsProject.instance()

#Access to layer by name
capa = proyecto.mapLayersByName('MUNICIPIO')[0] # returns a list with all layers or can be filtered by name

#properties of the layer
print('nombre: ', capa.name())
print('tipo: ', capa.type())
print('geometria: ', capa.geometryType())
print('EPSG: ', capa.crs().description())

marco = capa.extent()
print('marco: xmin: {}, ymin: {}, xmax: {}, ymax: {}'.format(marco.xMinimum(), marco.yMinimum(), marco.xMaximum(), marco.yMaximum()))
print('area: ', marco.area())
print('proveedor: ', capa.dataProvider().description())

"""
#with addMapLayer (through the project)
path1 = r'O:\nucleos.shp'
capa = QgsVectorLayer(path1,'NUCLEOS','ogr')

if capa.isValid():    
    proyecto.addMapLayer(capa)
else:
    print('Error al cargar la capa')

"""
