
# path to shp file
shp_path = r'O:\xxxxxxxx\PROVINCIA.shp'

#add layer to the project
capa = iface.addVectorLayer(shp_path,
                            'PROVINCIAS',
                            'ogr'
                            )
#zoom extension to all layers
iface.zoomFull()
