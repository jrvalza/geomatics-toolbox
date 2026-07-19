
"""
Edge Detection Application. Prewitt, Sobel, and Roberts Operators
"""

import os
import sys
import arcpy
import numpy as np
from arcpy.sa import *
from itertools import chain
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox

#===================================================================================
#===================================================================================

# py file path
py_path = os.path.dirname(__file__)

# ui file path

ui_name = os.path.join(py_path, "image_edge_user_gui.ui")

# load form
form_class = uic.loadUiType(ui_name)[0]

# dialog class
class MyDialogClass(QtWidgets.QDialog, form_class):
    # init function
    def __init__(self, parent=None):
        
        #User-defined attributes
        self.ruta_entrada = None
        self.ruta_salida =None
        self.name = None
        
        #kernels 3x3
        self.prewittV3 = np.array([[1,1,1], [0,0,0], [-1,-1,-1]])
        self.prewittH3 = self.prewittV3.T*-1
        self.sobelV3 = np.array([[1,2,1], [0,0,0], [-1,-2,-1]])
        self.sobelH3 = self.sobelV3.T*-1
        self.robertsV3 = np.array([[0,0,1], [0,0,0], [-1,0,0]])
        self.robertsH3 = np.rot90(self.robertsV3,k=1)

        #kernels 5X5
        self.prewittV5 = np.array([[2,2,2,2,2], [1,1,1,1,1], [0,0,0,0,0], [-1,-1,-1,-1,-1], [-2,-2,-2,-2,-2]])
        self.prewittH5 = self.prewittV5.T*-1
        self.sobelV5 = np.array([[1,2,3,2,1], [2,3,5,3,2], [0,0,0,0,0], [-2,-3,-5,-3,-2], [-1,-2,-3,-2,-1]])
        self.sobelH5=self.sobelV5.T*-1
        self.robertsV5 =np.array([[0,0,0,0,0], [0,0,0,1,0], [0,0,0,0,0], [0,-1,0,0,0], [0,0,0,0,0]])
        self.robertsH5=np.rot90(self.robertsV5,k=1)

        # init class dialog
        QtWidgets.QDialog.__init__(self, parent)
        
        # run dialog
        self.setupUi(self)
        
        #buttons
        self.btn_entrada.clicked.connect(self.entrada)
        self.btn_salida.clicked.connect(self.salida)
        self.btn_ejecutar.clicked.connect(self.ejecutar)
        self.btn_salir.clicked.connect(self.salirApp)
    
    # path to input image
    def entrada(self):
        fn = QFileDialog.getOpenFileName(parent = None,
                                        caption = 'Seleccione imagen',
                                        filter = '*.tif *.tiff')
        ruta = fn[0]
        if ruta:
            self.txt_entrada.setText(ruta)
            self.ruta_entrada = ruta
    
    # path to output directory
    def salida(self):
        fn = QFileDialog.getExistingDirectory(parent=None,
                                         caption='Directorio de salida')
        if fn:
            self.txt_salida.setText(fn)
            self.ruta_salida = fn

    # kernel coordinates from size (3 or 5)
    def _get_kernel_coordinates (self, n):
        coordinates = []
        increment = int((n-1)/2)
        for fila in range(n):
            f = fila-increment
            for colum in range(n):
                c = colum-increment
                coordinates.append((c,f))
        return coordinates
    
    # Initialize the application of the chosen filter
    def ejecutar(self):
        # Check input images and output directory
        if self.ruta_entrada:
            if self.ruta_salida:
                #Init 
                progress = 0 # execution progress
                out_extension = self.ruta_entrada.split('.')[-1] #image extension of the output image based on the extension of the input image

                #Obtaining the kernel and coordinate matrix from the selected size in the graphical interface
                filter_name= self.comboBox_filter.currentText()
                kernelSize= int(self.comboBox_kernel_size.currentText())
                kernel_coordinates = self._get_kernel_coordinates(kernelSize)
                
                if filter_name.lower() == 'sobel' and kernelSize == 3:
                    gradientX = np.array(list(chain(*self.sobelH3)))
                    gradientY = np.array(list(chain(*self.sobelV3)))
                if filter_name.lower() == 'sobel' and kernelSize == 5:
                    gradientX = np.array(list(chain(*self.sobelH5)))
                    gradientY = np.array(list(chain(*self.sobelV5)))

                if filter_name.lower() == 'prewitt' and kernelSize == 3:
                    gradientX = np.array(list(chain(*self.prewittH3)))
                    gradientY = np.array(list(chain(*self.prewittV3)))
                if filter_name.lower() == 'prewitt' and kernelSize == 5:
                    gradientX = np.array(list(chain(*self.prewittH5)))
                    gradientY = np.array(list(chain(*self.prewittV5)))

                if filter_name.lower() == 'roberts' and kernelSize == 3:
                    gradientX = np.array(list(chain(*self.robertsH3)))
                    gradientY = np.array(list(chain(*self.robertsV3)))
                if filter_name.lower() == 'roberts' and kernelSize == 5:
                    gradientX = np.array(list(chain(*self.robertsH5)))
                    gradientY = np.array(list(chain(*self.robertsV5)))
                
                progress+=5
                self.pb_progreso.setValue(progress)

                # load in memory the image using arcpy
                raster = arcpy.Raster(self.ruta_entrada)
                self.name = raster.name.split('.')[0]
                bands = raster.bandNames
                
                #Check that the chosen image is .tif or .tiff
                if raster.format.lower() not in ['tif', 'tiff']:
                    QMessageBox.warning(self, 'Advertencia', 'No se reconoce el formato de la imagen')
                    self.pb_progreso.setValue(0)
                else:
                    """
                    Configuración del raster de salida dependiendo del número de bandas de entrada.
                    Si la imagen es multiespectral, se asume que las bandas 0,1 y 2 son RGB y se obtiene una nueva imagen en escala de grises (luminancia).
                    """
                    #Single-band raster
                    if raster.bandCount==1:
                        raster_info = raster.getRasterInfo()
                        raster_info.setPixelType('F32') #F32 —32-bit floating point
                        raster_filtered = arcpy.Raster(raster_info)
                
                    #RGB raster is converted to grayscale (luminance)
                    if raster.bandCount>1:
                        #Assuming that the first three bands are R, G, and B, the conversion to luminance is performed.
                        raster = 0.299*raster.getRasterBands(bands[0]) + 0.587*raster.getRasterBands(bands[1]) + 0.114*raster.getRasterBands(bands[2])
                        raster_info=raster.getRasterInfo()
                        raster_info.setPixelType('F32') #F32 —32-bit floating point
                        raster_filtered = arcpy.Raster(raster_info)

                    
                    progress+=5
                    self.pb_progreso.setValue(progress)  

                    #Convolutions (horizontal and vertical gradients)
                    Gx_Gy = []
                    with RasterCellIterator({'rasters':[raster, raster_filtered]}) as rci:
                        #convolutional Kernels
                        directions = [gradientX, gradientY]

                        #variables to update the progress bar
                        total_pixels = raster.width * raster.height
                        progress_aument = 80 / (total_pixels*len(directions)) 

                        #Iterating by gradient direction (Gx and Gy)
                        for filter in directions:
                            #pixel iterator
                            for fila, columna in rci:
                                suma = 0
                                #Iterating by kernel coordinates
                                for idx, coords in enumerate(kernel_coordinates):
                                    #Kernel coordinates per pixel
                                    x = coords[0]
                                    y = coords[1]
                                    #filter value for each pixel
                                    weight = filter[idx]
                                    #Weighted sum of the neighborhood pixels (each pixel multiplied by the filter value)
                                    suma += raster[fila+x, columna+y]*weight 
                                #resulting value in the image for each pixel
                                raster_filtered[fila, columna] = suma

                                progress += progress_aument
                                self.pb_progreso.setValue(progress)

                            #convolution result (horizontal and vertical gradients)
                            Gx_Gy.append(raster_filtered)

                    self.pb_progreso.setValue(90)

                    #Absolute gradient as sum of pixels in absolute value
                    out_raster = np.abs(Gx_Gy[0]) + np.abs(Gx_Gy[1])
                    
                    self.pb_progreso.setValue(95)

                    #output raster
                    arcpy.env.workspace =self.ruta_salida
                    arcpy.env.overwriteOutput = True
                    out_raster.save(f'{self.name}_{filter_name}_{kernelSize}X{kernelSize}.{out_extension}')

                    self.pb_progreso.setValue(100)

                    #message of completion
                    QMessageBox.information(None, "Proceso", "Proceso terminado")
                    self.pb_progreso.setValue(0)
                
            else:
                QMessageBox.warning(self, 'Advertencia', 'Debe seleccionar una directorio de salida')
                self.pb_progreso.setValue(0)

        else:
            QMessageBox.warning(self, 'Advertencia', 'Debe seleccionar una imagen')
            self.pb_progreso.setValue(0)

    def salirApp(self):
        app.quit()
    
app = QtWidgets.QApplication(sys.argv)
myDialog = MyDialogClass(None)
myDialog.show()
app.exec_()


