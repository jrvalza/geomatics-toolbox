
#Canvas
mc = QgsMapCanvas()

#layer to add to the canvas (active layer)
capa = iface.activeLayer() #object type QgsMapLayer

#adding to the canvas
mc.setExtent(capa.extent())
mc.setLayers([capa])
mc.show()
