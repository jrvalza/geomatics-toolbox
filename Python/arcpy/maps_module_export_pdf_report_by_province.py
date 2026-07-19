
"""
Create a PDF for each province with the name, perimeter, and area
"""

import os
import arcpy
import arcpy.mp as mp

arcpy.env.workspace = r'C:\xxxxxxxxxxxxxxxx'

#project
aprx = mp.ArcGISProject(r'C:\xxxxxxxxx.aprx')


#map
mapa_detalle = aprx.listMaps('Detalle')[0]

#Layer
layer_prov = mapa_detalle.listLayers('PROVINCIA')[0]

#Layout   
layout = aprx.listLayouts('plantilla1 1')[0]
mf_detalle = layout.listElements('MAPFRAME_ELEMENT', 'Detalle')[0]
camara = mf_detalle.camera

#empty_pdf
pdf_DOC = mp.PDFDocumentCreate(r'C:\provincias.pdf')

#pdf provincias
with arcpy.da.SearchCursor(layer_prov, ['NOMBRE', 'SHAPE@']) as sc:
    for fila in sc:
        #Attributes
        nombre = fila[0]
        area = fila[1].area
        perimetro = fila[1].length
        marco = fila[1].extent        
        
        ##SELECT
        #query by attributte
        query = f""" "NOMBRE" = '{nombre}' """
        prov_sel = arcpy.SelectLayerByAttribute_management(in_layer_or_view=layer_prov,
                                                          selection_type="NEW_SELECTION",
                                                          where_clause=query)
        #zoom to select
        camara.setExtent(marco)

        #update texts elements in layout
        for texto in layout.listElements('TEXT_ELEMENT'):
            if texto.name == 'txt_nombre':
                texto.text = nombre

            if texto.name == 'txt_area':
                texto.text = f'{area/1000000:0.2f} km2'

            if texto.name == 'txt_perimetro':
                texto.text = f'{perimetro/1000:0.2f} km'

        #export pdf
        layout.exportToPDF(os.path.join(arcpy.env.workspace, f'plantilla1_{nombre}.pdf'))
        pdf_DOC.appendPages(os.path.join(arcpy.env.workspace, f'plantilla1_{nombre}.pdf'))

#close pdf
pdf_DOC.saveAndClose()

del aprx

print("Finalizado")
