
"""
Create a PDF by entity
"""

import os
import arcpy
import arcpy.mp as mp

arcpy.env.workspace = r'C:\xxxxxxxx'
arcpy.env.overwriteOutput = True
#project
aprx = mp.ArcGISProject(r'C:\xxxx.aprx')

#map
mapa_detalle = aprx.listMaps('Detalle')[0]

#Layer
layer_mun = mapa_detalle.listLayers('MUNICIPIO')[0]

#Layout   
layout = aprx.listLayouts('plantilla2 1')[0]
mf_detalle = layout.listElements('MAPFRAME_ELEMENT', 'Detalle')[0]
camara = mf_detalle.camera

#empty_pdf
pdf_DOC = mp.PDFDocumentCreate(r'C:\xxxxxxx.pdf')

#pdf municipios
with arcpy.da.SearchCursor(layer_mun, ['NOMBRE', 'POB95', 'POB91', 'SHAPE@']) as sc:
    count = 0
    for fila in sc:
        if count == 20:
            break
        #Attributes
        nombre = fila[0]
        pob95 = fila[1]
        pob91 = fila[2]
        marco = fila[3].extent        
        print(nombre)

        ##SELECT by attributte
        query = f""" "NOMBRE" = '{nombre}' """
        mun_sel = arcpy.SelectLayerByAttribute_management(in_layer_or_view=layer_mun,
                                                          selection_type="NEW_SELECTION",
                                                          where_clause=query)

        #zoom to select
        camara.setExtent(marco)

        #update texts elements in layout
        for texto in layout.listElements('TEXT_ELEMENT'):
            if texto.name == 'txt_nombre':
                texto.text = nombre

            if texto.name == 'txt_pob95':
                texto.text = pob95

            if texto.name == 'txt_pob91':
                texto.text = pob91

        #update rectangles in layout
        long_total = 0
        for bar_element in layout.listElements('GRAPHIC_ELEMENT'):
            if bar_element.name == 'bar_white_pob95':
                long_total = bar_element.elementWidth
        
        pob_total = pob95 + pob91
        pob95_proportion = pob95/pob_total
        pob91_proportion = pob91/pob_total

        for bar_element in layout.listElements('GRAPHIC_ELEMENT'):

            if bar_element.name == 'bar_blue_pob95':
                bar_element.elementWidth = long_total*pob95_proportion

            if bar_element.name == 'bar_blue_pob91':
                bar_element.elementWidth = long_total*pob91_proportion
            

        #export pdf
        layout.exportToPDF(os.path.join(arcpy.env.workspace, f'plantilla1_{nombre}.pdf'))
        pdf_DOC.appendPages(os.path.join(arcpy.env.workspace, f'plantilla1_{nombre}.pdf'))
        
        #Clear selectionquery by attributte
        mun_sel = arcpy.SelectLayerByAttribute_management(in_layer_or_view=layer_mun,
                                                          selection_type="CLEAR_SELECTION")
        count += 1
        

#close pdf
pdf_DOC.saveAndClose()

del aprx
print("Finalizado")
