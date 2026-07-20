
proyecto = QgsProject.instance()

#access to layer by name
capa = proyecto.mapLayersByName('PROVINCIA')[0]

for feat in capa.getFeatures():
    geom = feat.geometry()
    print (geom.wkbType())
    print ('Entidad: {}'.format(feat.id()))

    if geom.wkbType() == 1: #1->Point
        punto = geom.asPoint()
        print ('Punto : {0},{1}'.format(punto.x(),punto.y()))
        
    elif geom.wkbType() == 5: #1->multiLineString
        lineas = geom.asMultiPolyline()
        for linea in lineas:
            for punto in linea:
                 print ('Punto : {0},{1}'.format(punto.x(),punto.y()))
    
    elif geom.wkbType() == 6: #1->multiPolygon
        poligonos = geom.asMultiPolygon()
        for poligono in poligonos:
            print ('Anillos: {}'.format(len(poligono)))
            numero_anillo = 0
            for anillo in poligono:
                print ('Anillo: {}'.format(numero_anillo))
                numero_anillo += 1
                for punto in anillo:
                    print ('Punto : {0},{1}'.format(punto.x(),punto.y()))
    else:
        print ('Tipo desconocido')
