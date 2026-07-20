
import os

#Access to the QGIS project
pro = QgsProject.instance()

#layers of the project through mapLayers()
capas = pro.mapLayers()

#output file
path = r'O:\xxxxxxx.txt'
with open (path, 'w') as file:
    
    for capa in capas.values():
        nombre = capa.name()
        ruta = capa.source()
        tipo = capa.geometryType()
        if tipo == 0:
            tipo = 'puntos'
        if tipo == 1:
            tipo = 'lineas'
        if tipo == 2:
            tipo = 'poligonos'
            
        extension = ruta.split('\\')[-1].split('.')[1].lower()
        
        #save file
        file.write(f"\nNombre: {nombre}\nRuta: {ruta}\nTipo: {tipo}\nExtensión: {extension}\n")
        file.write('\n' + '*'*100 + '\n')
    
    file.close()
