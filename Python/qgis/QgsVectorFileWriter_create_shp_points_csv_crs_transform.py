
def leeCSV(fichero,pos = 0):
    datos = {}
    with open(fichero,'r') as f:
        for i in range(0,pos):
            next(f)
        for linea in f:
            partes = linea.split('\n')[0].split(';')
            iden = int(partes[0])
            cx = float(partes[1])
            cy = float(partes[2])
            datos[iden] = [cx,cy]
    f.close()
    return datos

def transforma(datos_31,proyecto):
    lista_trans = {}
    crs_origen = QgsCoordinateReferenceSystem(23031,QgsCoordinateReferenceSystem.EpsgCrsId)
    crs_destino = QgsCoordinateReferenceSystem(23030,QgsCoordinateReferenceSystem.EpsgCrsId)
    paso = QgsCoordinateTransform(crs_origen,crs_destino,proyecto)
    for iden in datos_31:
        lista = datos_31[iden]
        punto_origen = QgsPointXY(lista[0],lista[1])
        punto_destino = paso.transform(punto_origen)
        #print(punto_origen.x(),punto_origen.y())
        #print(punto_destino.x(),punto_destino.y())
        lista_trans[iden] = [punto_destino.x(),punto_destino.y()]
    return lista_trans
    
def creaShp(ruta):
    crs = QgsCoordinateReferenceSystem(23030,QgsCoordinateReferenceSystem.EpsgCrsId)
    campos = QgsFields()
    campo = QgsField('Vertice',QVariant.Int)
    campos.append(campo)
    shp = QgsVectorFileWriter(ruta,'latin-1',campos, QgsWkbTypes.Point,crs,'ESRI Shapefile')
    return shp
    
proyecto = QgsProject.instance()

datos_30 = leeCSV(r'O:\file1.csv',1)
datos_31 = leeCSV(r'O:\file2.csv',1)

datos_31_30 = transforma(datos_31,proyecto)
datos = dict(datos_30)
datos.update(datos_31_30)

ruta_shp = r'O:\vertices.shp'

shp = creaShp(ruta_shp)

for iden in datos:
    new_reg = QgsFeature()
    coords = datos[iden]
    cx = coords[0]
    cy = coords[1]
    punto = QgsGeometry.fromPointXY(QgsPointXY(cx,cy))
    new_reg.setGeometry(punto)
    new_reg.setAttributes([iden])
    shp.addFeature(new_reg)
del shp

iface.addVectorLayer(ruta_shp,'Vertices','ogr')
