
#access to the active layer
capa = iface.activeLayer() #object type QgsMapLayer

print("Nombre: ", capa.name())
print("Número de elementos: ", capa.featureCount())
