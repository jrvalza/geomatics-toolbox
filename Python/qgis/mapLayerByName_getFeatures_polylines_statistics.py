
import numpy as np

proyecto = QgsProject.instance()
capa = proyecto.mapLayersByName('Carreteras')[0]

longitudes = []

for reg in capa.getFeatures():
    geom = reg.geometry()
    longi = geom.length()
    longitudes.append(longi)

total = np.sum(longitudes)
media = np.mean(longitudes)
dt = np.std(longitudes)

print('Longitud total: '+str(total/1000.0)+' Km.')
print('Longitud media por tramo: '+str(media)+' m.')
print('Desv. típica: '+str(dt)+' m.')
