
'''
Contours generalization
'''

import processing

capa_input = iface.activeLayer()
capa_input.removeSelection()

#select one each two curves
cotas = []
for f in capa_input.getFeatures():
    cota = f.attribute('FIRST_Cota')
    cotas.append(cota)
cotas = list(set(cotas)) #list with unique elements
cotas.sort()
cotas_gen = []

for i in range(0,len(cotas),2):
    cotas_gen.append(cotas[i])

ids = []
for f in capa_input.getFeatures():
    cota = f.attribute('FIRST_Cota')
    if cota in cotas_gen:
        ids.append(f.id())
capa_input.select(ids)

#geoprocessing to simplify a line layer
output_path = r'C:\contours_gen.shp'
param_simp = {}
layer_source = capa_input.dataProvider().dataSourceUri()
param_simp['INPUT'] = QgsProcessingFeatureSourceDefinition(layer_source,selectedFeaturesOnly=True) #selectFeaturesOnly = True -> process only the selected features
param_simp['METHOD'] = 0
param_simp['TOLERANCE'] = 10 # meters
param_simp['OUTPUT'] = output_path 

processing.run('native:simplifygeometries',param_simp)

capa_gen = QgsVectorLayer(output_path,'contours_gen','ogr')
QgsProject().instance().addMapLayer(capa_gen)

#geoprocessing to smooth a line layer
output_path2 = r'C:\contours_smooth.shp'
param_smooth = {}
param_smooth['INPUT'] = output_path
param_smooth['ITERATIONS'] = 3
param_smooth['OFFSET'] = 0.25
param_smooth['MAX_ANGLE'] = 180.0
param_smooth['OUTPUT'] = output_path2

processing.run('native:smoothgeometry',param_smooth)

capa_smooth = QgsVectorLayer(output_path2,'contours_smooth','ogr')
QgsProject().instance().addMapLayer(capa_smooth)
