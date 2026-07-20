
from PyQt5.QtWidgets import QMessageBox

#Access to the QGIS project
pro = QgsProject.instance()

#layers of the project through mapLayers()
capas = pro.mapLayers()
name_capas = []
for capa in capas.values():
    name_capas.append(capa.name())

if len(name_capas) == 0:
    #warning window
    QMessageBox.warning(None, 'Capas', 'No se encontraron capas en el proyecto.')

else:
    #Message
    mensaje = f'El proyecto tiene {len(name_capas)} capas:' + '\n'\
            f'- {name_capas[0]}' + '\n'\
            f'- {name_capas[1]}' + '\n'\
            f'- {name_capas[2]}'

    #Information window
    QMessageBox.information(None, 'Capas', mensaje )
