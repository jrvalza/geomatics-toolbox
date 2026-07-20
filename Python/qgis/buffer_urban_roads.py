"""
Calculating the length of roads within a 1 km buffer around urban centers using QGIS geoprocessing tools
"""

from PyQt5.QtCore import QVariant

proyecto = QgsProject.instance()

#=========================================================================================
#=================================Buffer around urban centers=============================
#=========================================================================================

#access to urban NUCLEOS
capa_nucleos = proyecto.mapLayersByName('NUCLEOS')[0]

#Access to the data provider
dp = capa_nucleos.dataProvider()

#Creating the output layer
shp = r"O:\xxxxxx.shp" 

#NUCLEO 'Name' field in the output layer
campos = QgsFields()
campos.append(QgsField("NOMBRE",QVariant.String))

#Creating the layer in disk
shp_writer = QgsVectorFileWriter(shp,"CP1250",campos,QgsWkbTypes.Polygon,dp.crs(),"ESRI Shapefile")


#Checking for errors while creating the output buffer layer
if shp_writer.hasError() != QgsVectorFileWriter.NoError:
    print ("Error al crear la capa: ", shp_writer.hasError(), shp_writer.errorMessage())
    #Removal of the reference to the layer
    del shp_writer

#if no error, the buffer is created
else:
    #beginning to iterate through the features of the NUCLEOS layer
    for feat in capa_nucleos.getFeatures():
        #Access to the geometry and the NOMBRE attribute
        geom = feat.geometry()
        nucleo_name = feat.attribute('NOMBRE')

        #Checking that the geometry is not null
        if geom != None:
            #Creation of the buffer (radius and segment length)
            b = geom.buffer(1000,50)

            #Creation of a new feature to add to the output layer
            nueva_feat = QgsFeature()

            #Assignment of the geometry from the buffer
            nueva_feat.setGeometry(b)

            #Filling the NOMBRE attribute
            nueva_feat.setAttributes([nucleo_name])

            #Adding the new feature to the output shapefile
            shp_writer.addFeature(nueva_feat)

    #Removing the reference to the layer
    del shp_writer

    #Loading the layer in QGIS
    capa_buffer = QgsVectorLayer(shp,"Buffer_nucleos","ogr")
    proyecto.addMapLayer(capa_buffer)

#=========================================================================================
#=================Intersection of the 'buffer' layer with the road layer==================
#=========================================================================================

#input layer
capa_carretera = proyecto.mapLayersByName('CARRETERA')[0]

#overlay layer
capa_buffer_nucleos = proyecto.mapLayersByName('Buffer_nucleos')[0]

#output layer
shp_path = r"O:\xxxxxxxxx.shp"

#Intersection geoprocess (extracting road geometries that intersect with the polygons in the buffer layer)
param_simp = {}
param_simp['INPUT']= capa_carretera
param_simp['OVERLAY']= capa_buffer_nucleos
param_simp['INPUT_FIELDS']=[]
param_simp['OVERLAY_FIELDS']=[]
param_simp['OVERLAY_FIELDS_PREFIX']=''
param_simp['OUTPUT']= shp_path
param_simp['GRID_SIZE']=None
processing.run("native:intersection",param_simp)

#The intersection result is loaded into QGIS
capa_intersection = QgsVectorLayer(shp_path,"nucleos_carretras_intersect","ogr")
proyecto.addMapLayer(capa_intersection)


#=========================================================================================
#===================Calculation of lengths (by NUCLEO) and display on screen==============
#=========================================================================================

#The previously obtained layer (intersections) is read from the project
capa_carretera_intersect = proyecto.mapLayersByName('nucleos_carretras_intersect')[0]

#We begin by iterating over each feature in the 'NUCLEOS' buffer layer
for feat in capa_buffer_nucleos.getFeatures():
    #Remove the current selections from the intersection layer
    capa_carretera_intersect.removeSelection()

    #the geometry of the 'NUCLEO' is obtained
    geom_nucleo = feat.geometry()

    #An empty list is initialized to store the identifiers of the road segments
    #contained in each 'NUCLEO'; the 'intersects' predicate is used

    ids = []

    #Iterate through the roads to identify which ones are included in each 'NUCLEO'
    for carretera in capa_carretera_intersect.getFeatures():
        #the geometry of the road section is obtained
        geom_carretera = carretera.geometry()

        #verify if the geometries (NUCELO and road) intersect
        #if so, save the identifier of the road section
        if geom_nucleo.intersects(geom_carretera):
            ids.append(carretera.id())

    #Road segments are selected by identifier
    capa_carretera_intersect.select(ids)

    #Iterate over the selection of road segments to sum the length and obtain the desired result
    longitud = 0
    for tramo in capa_carretera_intersect.getSelectedFeatures():
        tramo_geom = tramo.geometry()
        tramo_longitud = tramo_geom.length()
        longitud += tramo_longitud

    #Output
    nucleo_name = feat.attribute('NOMBRE')
    print(f"Nombre: {nucleo_name}, Longitud: {longitud/1000:0.2f} km")

print('Proceso terminado.')

