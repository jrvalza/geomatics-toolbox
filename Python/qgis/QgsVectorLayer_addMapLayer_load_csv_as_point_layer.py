
#project
proyecto = QgsProject.instance()

#INIT
path = r'O:\xxxxxxxxxx.csv'
delimiter = ';'
xfield = 'X'
yfield = 'Y'
EPSG = 23030

#with addMapLayer (through the project)
uri = f'file:///{path}?delimiter={delimiter}&xField={xfield}&yField={yfield}&crs=epsg:{EPSG}'
capa = QgsVectorLayer(uri,'VERTICES', "delimitedtext")

# is valid?
if capa.isValid():    
    proyecto.addMapLayer(capa)
else:
    print('Error al cargar la capa')
