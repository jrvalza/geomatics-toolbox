
"""
Text report generator with project content: layers, types, and paths
"""

import arcpy.mp as mp
import os
from datetime import datetime

def cabeceraProyecto(archivo, nombre_aprx, fuente_aprx, n_mapas):
    archivo.write(60*'*'+'\n')
    archivo.write(f'Proyecto: {nombre_aprx} '+'\n')
    archivo.write(f'Ruta: {fuente_aprx} '+'\n')
    archivo.write(f'Número de mapas: {n_mapas} '+'\n')
    archivo.write(60*'*'+'\n')
    archivo.write(2*'\n')

def cabeceraMapa(archivo, nombre_mapa, n_capas):
    archivo.write(60*'*'+'\n')
    archivo.write(f'Mapa: {nombre_mapa} '+'\n')
    archivo.write(f'Número de capas: {n_capas} '+'\n')
    archivo.write(60*'*'+'\n')

def cuerpoMapa(archivo, capas):
    for capa in capas:
        if capa.isFeatureLayer:
            archivo.write(f'Capa: {capa.name} . Tipo: vectorial'+'\n')
            archivo.write(60*'-'+'\n')
        if capa.isRasterLayer:
            archivo.write(f'Capa: {capa.name} . Tipo: raster'+'\n')
            archivo.write(60*'-'+'\n')
        if capa.isBasemapLayer:
            archivo.write(f'Capa: {capa.name} . Tipo: capa base'+'\n')
            archivo.write(60*'-'+'\n')
    archivo.write(60*'*'+'\n')
    archivo.write(2*'\n')

def pieInforme(archivo):
    archivo.write('Final del informe'+'\n')
    archivo.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S)"))

ruta_aprx = r'C:\xxxxxx.aprx'
informe = r'C:\xxxxxxx.txt'

with open(informe, 'w', encoding='utf-8') as archivo:

    aprx = mp.ArcGISProject(ruta_aprx)
    fuente_aprx = aprx.filePath
    nombre_aprx = os.path.basename(fuente_aprx)

    mapas = aprx.listMaps()
    n_mapas = len(mapas)

    cabeceraProyecto(archivo, nombre_aprx, fuente_aprx, n_mapas)

    for mapa in mapas:
        nombre_mapa = mapa.name
        capas = mapa.listLayers()
        n_capas = len(capas)
        cabeceraMapa(archivo, nombre_mapa, n_capas)
        cuerpoMapa(archivo, capas)

    pieInforme(archivo)
    del aprx

print('Informe creado')
