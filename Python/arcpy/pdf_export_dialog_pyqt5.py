
import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import arcpy
import arcpy.mp as mp
arcpy.env.overwriteOutput = True

#===================================================================================
#================================Access layer=======================================
#===================================================================================
#project
aprx = mp.ArcGISProject(r'C:\xxxxxxxx.aprx')
#map
mapa_detalle = aprx.listMaps('Detalle')[0]
#Layer
layer_mun = mapa_detalle.listLayers('MUNICIPIO')[0]
#Layout   
layout = aprx.listLayouts('plantilla1 1')[0]
mf_detalle = layout.listElements('MAPFRAME_ELEMENT', 'Detalle')[0]
camara = mf_detalle.camera
#===================================================================================
#===================================================================================

# py file path
py_path = os.path.dirname(__file__)

# ui file path
ui_name = os.path.join(py_path, "pdf_export_dialog_gui.ui")

# load form
form_class = uic.loadUiType(ui_name)[0]

# dialog class
class MyDialogClass(QtWidgets.QDialog, form_class):
    # init function
    def __init__(self, parent=None):
        
        #user attribute
        self.ruta_salida =None

        # init class dialog
        QtWidgets.QDialog.__init__(self, parent)
        
        # run dialog
        self.setupUi(self)
        
        #init list municipios
        self.inicializa()
                
        #buttons
        self.btn_salida.clicked.connect(self.salida)
        self.btn_ejecutar.clicked.connect(self.ejecutar)
        self.btn_salir.clicked.connect(self.salirApp)
    
    def inicializa(self):
        with arcpy.da.SearchCursor(layer_mun, ['NOMBRE']) as sc:
            for fila in sc:
                self.comboBox.addItem(str(fila[0]))

    def salida(self):
        fn = QFileDialog.getSaveFileName(parent = None,
                                        caption = 'Guardar pdf',
                                        filter = '*.pdf')
        ruta = fn[0]
        if ruta:
            self.txt_salida.setText(ruta)
            self.ruta_salida = ruta


    def ejecutar(self):
        #current selected municipio
        municipio = self.comboBox.currentText()
        self.pb_progreso.setValue(25)
        
        ##SELECT
        #query by attributte
        query = f""" "NOMBRE" = '{municipio}' """
        mun_sel = arcpy.SelectLayerByAttribute_management(in_layer_or_view=layer_mun,
                                                          selection_type="NEW_SELECTION",
                                                          where_clause=query)
        self.pb_progreso.setValue(50)

        #pdf
        with arcpy.da.SearchCursor(layer_mun, ['SHAPE@']) as sc:
            for fila in sc:
                #Attributes
                nombre = municipio
                area = fila[0].area
                perimetro = fila[0].length
                marco = fila[0].extent        
        
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
            
            self.pb_progreso.setValue(75)
        
            #export pdf
            if self.ruta_salida:
                layout.exportToPDF(self.txt_salida.text())

                #Clear selectionquery by attributte
                arcpy.SelectLayerByAttribute_management(in_layer_or_view=layer_mun,
                                                        selection_type="CLEAR_SELECTION")
        
                self.pb_progreso.setValue(100)
                
                QMessageBox.information(None, "Proceso", "Proceso terminado")
            else:
                QMessageBox.warning(self, 'Advertencia', 'Debe seleccionar una ruta de salida')
                self.pb_progreso.setValue(0)


    def salirApp(self):
        app.quit()
    
app = QtWidgets.QApplication(sys.argv)
myDialog = MyDialogClass(None)
myDialog.show()
app.exec_()

del aprx
