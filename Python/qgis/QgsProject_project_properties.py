
import os
import sys

#Access to the QGIS project
pro = QgsProject.instance()

print("Nombre: ", pro.baseName())
print("ruta del proyecto: ", pro.fileName())
print("Titulo del proyecto: ", pro.title())

carpeta = os.path.dirname(pro.fileName())
print("ruta del proyecto: ", carpeta)

print(sys.path)
