
import arcpy
import arcpy.mp as mp

#project
aprx = mp.ArcGISProject(r'C:\xxxxxxxxxx.aprx')

#layouts
layout = aprx.listLayouts('plantilla1')[0]

#Mapframe
mf_detalle = layout.listElements('MAPFRAME_ELEMENT', 'Detalle')[0]

#camera
camara = mf_detalle.camera
camara.scale = 500000
#save project
layout.exportToPDF(r'C:\500000.pdf')

camara.scale = 1000000
#save project
layout.exportToPDF(r'C:\1000000.pdf')

camara.scale = 1500000
#save project
layout.exportToPDF(r'C:\1500000.pdf')

#empty_pdf
pdf_DOC = mp.PDFDocumentCreate(r'C:\maps.pdf')

#adding pages
pdf_DOC.appendPages(r'C:\500000.pdf')
pdf_DOC.appendPages(r'C:\1000000.pdf')
pdf_DOC.appendPages(r'C:\1500000.pdf')

#close pdf
pdf_DOC.saveAndClose()

del aprx
del pdf_DOC

print("Proceso finalizado")
