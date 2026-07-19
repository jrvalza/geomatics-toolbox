
import arcpy

if arcpy.CheckExtension('3D') == 'Available':
    arcpy.CheckOutExtension('3D')

    #Operations with the 3D Analyst extension

    arcpy.CheckInExtension('3D')
else:
    print("La extension 3D no esta disponible")
