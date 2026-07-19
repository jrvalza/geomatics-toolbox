
"""
TIN empty
"""

import arcpy

arcpy.env.workspace = r'C:\xxxxxxx'
arcpy.env.overwriteOutput = True

#Template for license management
if arcpy.CheckExtension('3D') == 'Available':
    arcpy.CheckOutExtension('3D')

    arcpy.CreateTin_3d('tin_64032')

    arcpy.CheckInExtension('3D')
else:
    print("La extension 3D no esta disponible")

print("TIN creado")
