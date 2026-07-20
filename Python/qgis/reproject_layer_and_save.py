
ruta = r'C:\xxxxx.shp'

proyecto = QgsProject.instance()

capa = proyecto.mapLayersByName('MUNICIPIO')[0]

crs_origen = capa.dataProvider().crs()

#output CRS
crs_destino = QgsCoordinateReferenceSystem(23031,QgsCoordinateReferenceSystem.EpsgCrsId)

paso = QgsCoordinateTransform(crs_origen,crs_destino,proyecto)

#create layer projected
error  =QgsVectorFileWriter.writeAsVectorFormat(capa, ruta, "CP1250", paso, "ESRI Shapefile")
if error == QgsVectorFileWriter.NoError:
    
    #load layer in QGIS
    capa_buffer = QgsVectorLayer(ruta,"est_23031","ogr")
    proyecto.addMapLayer(capa_buffer)
else:
    print ('Error al cargar la capa')
