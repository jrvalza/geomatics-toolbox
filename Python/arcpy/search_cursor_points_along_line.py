
"""
Create a "points_km" layer with one point every kilometer along Autovia A3
"""

import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

pto_km = []
with arcpy.da.SearchCursor('Autovia_A3.shp', 'SHAPE@') as sc:
    for fila in sc:
        geom = fila[0] 

        #Init long road
        long_total = geom.length
        increment = 1000
        
        #Initial point on road
        p_init = geom.positionAlongLine(value=0)
        pto_km.append(p_init)

        #Points km
        while long_total>1000:
              p = geom.positionAlongLine(value=long_total)
              pto_km.append(p)
              long_total -= increment
        
        #Last point on road
        p_last = geom.positionAlongLine(value=long_total)
        pto_km.append(p_last)

#Output shp
arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.CopyFeatures_management(pto_km, 'A3_ptos_km.shp')

print('Proceso terminado.')

