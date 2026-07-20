
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *

def run_script(iface):

    capa = iface.activeLayer() #object type QgsMapLayer

    print("Nombre: ", capa.name())

    print("Número de elementos: ", capa.featureCount())


