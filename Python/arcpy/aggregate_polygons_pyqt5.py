
import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import arcpy
import arcpy.mp as mp
arcpy.env.overwriteOutput = True

# py file path
py_path = os.path.dirname(__file__)

# ui file path
ui_name = os.path.join(py_path, "aggregate_polygons_gui.ui")

# load form
form_class = uic.loadUiType(ui_name)[0]

# dialog class
class MyDialogClass(QtWidgets.QDialog, form_class):
    # init function
    def __init__(self, parent=None):
        
        # init class dialog
        QtWidgets.QDialog.__init__(self, parent)
        
        # run dialog
        self.setupUi(self)

        #Check input data
        self.txt_dist.setValidator(QDoubleValidator())
        self.txt_tol.setValidator(QDoubleValidator())
        
        #init dist and tol
        self.inicializa()

        #buttons
        self.btn_entrada.clicked.connect(self.entrada)
        self.btn_salida.clicked.connect(self.salida)
        self.btn_ejecutar.clicked.connect(self.ejecutar)
        self.btn_salir.clicked.connect(self.salirApp)

    def entrada(self):
        fn = QFileDialog.getOpenFileName(parent = None,
                                        caption = 'Capa de entrada',
                                        filter = '*.shp')
        ruta = fn[0]
        if ruta:
            self.txt_entrada.setText(ruta)


    def salida(self):
        fn = QFileDialog.getSaveFileName(parent = None,
                                        caption = 'Capa de salida',
                                        filter = '*.shp')
        ruta = fn[0]
        if ruta:
            self.txt_salida.setText(ruta)

    def inicializa(self):
        self.txt_dist.setText(str(10))
        self.txt_tol.setText(str(10))
        
    def ejecutar(self):
        capa_entrada = self.txt_entrada.text()
        capa_salida = self.txt_salida.text()
        distancia_buffer = float(self.txt_dist.text())
        tolerancia = float(self.txt_tol.text())
        
        #Geoprocessing
        #1-)buffer
        capa_intermedia = os.path.join(os.path.dirname(capa_entrada), 'remove.shp')
        arcpy.Buffer_analysis(in_features = capa_entrada,
                      out_feature_class = capa_intermedia,
                      buffer_distance_or_field = distancia_buffer,
                      dissolve_option = 'ALL')
        
        self.pb_progreso.setValue(25)
        
        #2-)inverse buffer
        arcpy.Buffer_analysis(in_features = capa_intermedia,
                      out_feature_class = capa_salida,
                      buffer_distance_or_field = distancia_buffer * -1,
                      )

        self.pb_progreso.setValue(50)

        #3-)generalize
        arcpy.Generalize_edit(in_features = capa_salida,
                              tolerance = tolerancia
                              )
        
        self.pb_progreso.setValue(75)
        #delete temporal data
        arcpy.Delete_management(in_data = capa_intermedia)

        self.pb_progreso.setValue(100)

        QMessageBox.information(None, "Proceso", "Proceso terminado")
        
    def salirApp(self):
        app.quit()
    
app = QtWidgets.QApplication(sys.argv)
myDialog = MyDialogClass(None)
myDialog.show()
app.exec_()
