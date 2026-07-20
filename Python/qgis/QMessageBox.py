
import os
from PyQt5.QtWidgets import QMessageBox

#Access to the QGIS project
pro = QgsProject.instance()

#Menssage to show
carpeta = os.path.dirname(pro.fileName())
mensaje = f'Nombre: {pro.baseName()}' + '\n'\
          f'Ruta: {pro.fileName()}' + '\n'\
          f'Carpeta: {carpeta}' + '\n'\
          f'Titulo: {pro.title()}'

#information window
QMessageBox.information(None, 'Información', mensaje )

#warning window
QMessageBox.warning(None, 'Información', mensaje )

#error window
QMessageBox.critical(None, 'Información', mensaje )
