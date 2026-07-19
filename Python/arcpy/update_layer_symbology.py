
import arcpy.mp as mp

aprx_path = r'C:\xxxxxx.aprx'

# Access layer
aprx = mp.ArcGISProject(aprx_path)

# color ramp names
# color_ramps = aprx.listColorRamps()
# for cr in color_ramps:
#     print(cr.name)+

mapa = aprx.listMaps()[0] # map access
capa_mun = mapa.listLayers()[0] # layer access

# symbology
sym = capa_mun.symbology # layer symbology
ren = sym.renderer

# change symbology
ren.classificationMethod = 'NaturalBreaks'
ren.breakCount = 6
ren.classificationField = 'POB95'
ren.colorRamp = aprx.listColorRamps('Cyan to Purple')[0]

# update symbology
sym.renderer = ren 
capa_mun.symbology = sym

# save project
aprx.save()

del aprx

