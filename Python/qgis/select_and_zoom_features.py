
proyecto = QgsProject.instance()

#Access to layer by name
capa = proyecto.mapLayersByName('MUNICIPIO')[0]

#Select in the map

#all records
capa.selectAll()

#invert selection
capa.invertSelection()

#deselect all
capa.removeSelection()

#select by identifier
capa.select(list(range(100,500)))

#count the number of selected elements
print(capa.selectedFeatureCount())

#zoom to a selection (boundingBox of the selection)
capa.removeSelection()
capa.select(10)
marco = capa.boundingBoxOfSelected()

print (marco.xMinimum(), marco.yMinimum(),marco.xMaximum(), marco.yMaximum())
iface.mapCanvas().setExtent(marco) #Canvas extension


marco = QgsRectangle(344093.984033, 4583913.0, 373119.96416, 4614689.76336)
capa.selectByRect(marco, True) #->True: add to selection
marco = capa.boundingBoxOfSelected()

print (marco.xMinimum(), marco.yMinimum(),marco.xMaximum(), marco.yMaximum())
iface.mapCanvas().setExtent(marco) #Canvas extension
