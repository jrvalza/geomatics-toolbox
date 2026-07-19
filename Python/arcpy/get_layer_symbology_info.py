
import arcpy.mp as mp

aprx_path = r'C:\xxxxxx.aprx'

# Access layer
aprx = mp.ArcGISProject(aprx_path)
mapa = aprx.listMaps()[0] # map access
capa_mun = mapa.listLayers()[0] # layer access

# symbology
sym = capa_mun.symbology # layer symbology
ren = sym.renderer

print(f'Type symbology: {ren.type}')
print(f'Classification Method: {ren.classificationMethod}')
print(f'Number of clasess: {ren.breakCount}')
print(f'Classification field: {ren.classificationField}')
