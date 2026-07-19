
'''
Problem: in a folder where all the shp files share the same coordinate system,
only some of them have a prj file. This script adds that prj file to the rest of the shp files if they don't have it.
'''

import os
import arcpy
import shutil
from glob import glob

def checkPRJ(shp):
    """Check if the shp file has a projection file (.prj)
    Args:
        shp (str): path to the shp file

    Returns:
        boolean: if False, the shp does not have a prj file
    """
    nombre = os.path.basename(shp).split(".")[0]
    carpeta = os.path.dirname(shp)
    ruta_prj = os.path.join(carpeta, nombre+'.prj')
    if arcpy.Exists(ruta_prj):
        return True
    else:
        return False


def copyPRJ(prj_base, shp):
    """Copy the prj file with the name of the shp
    Args:
        prj_base (string): path to the base .prj file
        shp (string): path to the shp file
    """
    nombre = os.path.basename(shp).split(".")[0]
    carpeta = os.path.dirname(shp)
    nuevo_prj = os.path.join(carpeta, nombre+'.prj')
    
    # Copy a file to a new location with a different name
    shutil.copy2(prj_base, nuevo_prj)

entrada = r'C:\xxxxxx'
prj_base = r'C:\xxxxxx.prj'
shp_list = glob(entrada+'\\*.shp')

for shp in shp_list:
    if not checkPRJ(shp):
        copyPRJ(prj_base, shp)

print('Proceso terminado')
