
proyecto = QgsProject().instance()

capa = proyecto.mapLayersByName('FERROCARRIL')[0]

# create a shapefile
shp_path = r'C:\xxxxxxxxx.shp'
cod_field = 'CP1250' # 'utf-8'
campos = QgsFields()
campo = QgsField('Buff_dist',QVariant.Double,len=10,prec=3)
campos.append(campo)
tipo = QgsWkbTypes.Polygon
crs = capa.dataProvider().crs()
driver = 'ESRI shapefile'
shp_out = QgsVectorFileWriter(shp_path,cod_field,campos,tipo,crs,driver)

# read the features of the layer and create the buffer
for f in capa.getFeatures():
    geom = f.geometry()
    buf = geom.buffer(1000,50)
    new_f = QgsFeature()
    new_f.setGeometry(buf)
    new_f.setAttributes([1000])
    shp_out.addFeature(new_f)

#add layer to project
new_capa = QgsVectorLayer(shp_path,'Buffer_1000','ogr')
proyecto.addMapLayer(new_capa)

del shp_out
