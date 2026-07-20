
proyecto = QgsProject.instance()

capa = proyecto.mapLayersByName('MUNICIPIO')[0]

#Access to the CRS of the layer
dp = capa.dataProvider()
crs_origen = dp.crs()

#Point of origin
punto_origen = QgsPointXY(354403,4613781)

#Definition of the target CRS
crs_destino = QgsCoordinateReferenceSystem(25830,QgsCoordinateReferenceSystem.EpsgCrsId)

#Definition of the transformation system
paso = QgsCoordinateTransform(crs_origen,crs_destino,proyecto)

#Application of the transformation
punto_destino = paso.transform(punto_origen)

#output
print ("Punto origen: {},{}".format(punto_origen.x(),punto_origen.y()))
print ("Punto destino: {},{}".format(punto_destino.x(),punto_destino.y()))
