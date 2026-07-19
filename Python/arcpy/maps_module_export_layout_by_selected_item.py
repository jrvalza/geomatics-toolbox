
import arcpy
import arcpy.mp as mp

#project
aprx = mp.ArcGISProject(r'C:\xxxxxxxxxxx.aprx')

#map
mapa_detalle = aprx.listMaps('Detalle')[0]

#Layer
layer_mun = mapa_detalle.listLayers('MUNICIPIO')[0]

##SELECT ONE MUNICIPIO
#query by attributte
query = """ "NOMBRE" = 'Villadiego' """

mun_sel = arcpy.SelectLayerByAttribute_management(in_layer_or_view=layer_mun,
                                                  selection_type="NEW_SELECTION",
                                                  where_clause=query)
with arcpy.da.SearchCursor(mun_sel, ['NOMBRE', 'POB95', 'SHAPE@']) as sc:
    for fila in sc:
        nombre = fila[0]
        pob95 = fila[1]
        marco = fila[2].extent

##UPDATE LAYOUT   
layout = aprx.listLayouts('plantilla1')[0]
mf_detalle = layout.listElements('MAPFRAME_ELEMENT', 'Detalle')[0]
camara = mf_detalle.camera

#zoom
camara.setExtent(marco)

#update texts elements in layout
for texto in layout.listElements('TEXT_ELEMENT'):
    if texto.name == 'txt_nombre':
        texto.text = nombre

    if texto.name == 'txt_pob95':
        texto.text = pob95

#export pdf
layout.exportToPDF(r'C:\mun_Sel.pdf')

del aprx
