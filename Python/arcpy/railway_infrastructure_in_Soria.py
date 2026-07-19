
"""
Overview of the railway infrastructure in the province of SORIA
"""

import os
import arcpy
import arcpy.mp as mp

#Output directory
arcpy.env.workspace = r'C:\Projects\xxxxxx'

#project file (aprx)
aprx = mp.ArcGISProject(r'C:\Projects\xxxxxx.aprx')


#detailed map
mapa_detalle = aprx.listMaps('mapa_detalle')[0]

#Layers on the 'mapa_detalle' map
layer_prov = mapa_detalle.listLayers('PROVINCIA')[0]
layer_ferro = mapa_detalle.listLayers('FERROCARRIL')[0]
layer_est = mapa_detalle.listLayers('ESTACIONES')[0]


##SELECT PROVINCIA SORIA
#Filter by the 'NOMBRE' attribute in the province layer
nombre = 'SORIA'
query = f""" "NOMBRE" = '{nombre}' """
prov_sel = arcpy.SelectLayerByAttribute_management(in_layer_or_view=layer_prov,
                                                   selection_type="NEW_SELECTION",
                                                   where_clause=query)

#Selection by location of the stations and railway lines that intersect with the previously selected province
ferro_sel = arcpy.SelectLayerByLocation_management(layer_ferro, 'INTERSECT', layer_prov, selection_type='NEW_SELECTION')
est_sel = arcpy.SelectLayerByLocation_management(layer_est, 'INTERSECT', layer_prov, selection_type='NEW_SELECTION')


#Drawing template showing the elements to be updated
layout = aprx.listLayouts('plantilla1 1')[0]
mf_detalle = layout.listElements('MAPFRAME_ELEMENT', 'mapa_detalle')[0]
camara = mf_detalle.camera

#=======================================================================================================
#====================================Data to update the template========================================
#=======================================================================================================
#Retrieving data for the selected province (name and extension)
with arcpy.da.SearchCursor(layer_prov, ['NOMBRE', 'SHAPE@']) as sc:
    for fila in sc:
        #Attributes
        nombre = fila[0]
        marco = fila[1].extent        

#Calculating the total length of the railroad lines located within the selected province
with arcpy.da.SearchCursor(layer_ferro, ['SHAPE@']) as sc:
    longitud = 0
    for fila in sc:
        #Attributes
        longitud += fila[0].length  
#Deselect railroad lines
arcpy.SelectLayerByAttribute_management(in_layer_or_view=layer_ferro,
                                        selection_type="CLEAR_SELECTION")

#Obtaining the number of stations in the selected province
n_est = arcpy.GetCount_management(layer_est) 
#=======================================================================================================
#=======================================================================================================

#Zoom in on the selected province
camara.setExtent(marco)

#Updating text elements in the template
for texto in layout.listElements('TEXT_ELEMENT'):
    if texto.name == 'txt_nombre':
        texto.text = nombre

    if texto.name == 'txt_longitud':
        texto.text = f'{longitud/1000:0.2f}'

    if texto.name == 'txt_num_est':
        texto.text = f'{n_est}'

#Exporting the PDF file
layout.exportToPDF(os.path.join(arcpy.env.workspace, f'plantilla1_{nombre}.pdf'))

#completed
del aprx
print("Finalizado")

