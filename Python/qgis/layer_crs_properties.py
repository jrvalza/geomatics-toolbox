
proyecto = QgsProject.instance()

capa = proyecto.mapLayersByName('MUNICIPIO')[0]

#units dictionary
unidades = {0:'Metros',
            1:'Pies',
            2:'Grados',
            3:'Desconocido',
            4:'Grados decimales',
            5:'Grados minutos y segundos',
            6:'Grados y minutos decimales',
            7:'Millas náuticas'
            }

dp = capa.dataProvider()
crs = dp.crs()

print ("QGIS CRS ID: ", crs.srsid())
print ("PostGIS SRID: ", crs.postgisSrid())
print ("EPSG ID: ",crs.authid())
print ("Description:", crs.description())
print ("Projection Acronym:", crs.projectionAcronym())
print ("Ellipsoid Acronym:", crs.ellipsoidAcronym())
print ("Proj4 String:", crs.toProj4())
print ("Wkt String:", crs.toWkt())

#geographical system or projected system
print ("Is geographic:", crs.isGeographic())

#CRS units (values defined in QGis::units enum)
print ("Map units:", unidades[crs.mapUnits()])
