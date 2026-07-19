
import arcpy

#workspace definition
arcpy.env.workspace = r'C:\xxxxxx'
arcpy.env.overwriteOutput = True

#=============================================================
# Read points
#=============================================================
with arcpy.da.SearchCursor('nucleos.shp', 'SHAPE@') as sc:
    for fila in sc:
        geom = fila[0]
        #punto = geom.firstPoint
        for punto in geom:
            print(punto.X, punto.Y)

print('Done')

#=============================================================
# Read polylines
#=============================================================
with arcpy.da.SearchCursor('carretera.shp', 'SHAPE@') as sc:
    id = 0
    for fila in sc:
        id +=1
        geom = fila[0]
        #punto = geom.firstPoint
        for parte in geom:
            print('\nNueva polilinea')
            for point in parte:
                print(point.X, point.Y)
        if id == 10:
            break

print('Done')

#=============================================================
# Read polygons
#=============================================================
with arcpy.da.SearchCursor('polygons_agujero.shp', 'SHAPE@') as sc:
    for fila in sc:
        geom = fila[0] #polygon
        
        for parte in geom:
            print('\nNueva poligono')
            for point in parte:
                if point:
                    print(point.X, point.Y)
                else:
                    print('Anillo')

print('Done')
