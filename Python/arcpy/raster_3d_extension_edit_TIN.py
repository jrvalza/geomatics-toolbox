
import arcpy

arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

path_cotas = r"C:\puntos_cota.shp"
path_cn = r"C:\curvas_nivel.shp"
path_bl = r"C:\hidrog_lin.shp"

#licence
if arcpy.CheckExtension('3D') == 'Available':
    arcpy.CheckOutExtension('3D')    
    '''
    masspoints = puntos de cota
    softlines = curvas de nivel
    hardlines = lineas de ruptura
    [capa, campo de cotas, etiqueta para triangulos, tipo de tratamiento, Z como altitud]
    '''
    entities = [[path_cotas, 'COTA', '<None>', 'masspoints', False],
                [path_cn, 'COTA', '<None>', 'softline', False],
                [path_bl, '<None>', '<None>', 'hardline', True]] 
    
    arcpy.EditTin_3d('tin_64032', entities, True)

    arcpy.CheckInExtension('3D')
else:
    print("La extension 3D no esta disponible")

print("TIN Editado")
