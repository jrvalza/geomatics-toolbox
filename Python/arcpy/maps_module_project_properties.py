
'''
In the Python console within ArcGIS Pro

import arcpy
import arcpy.mp as mp #modulo de mapas
aprx = mp.ArcGISProject('CURRENT')
'''

import sys
import arcpy
import arcpy.mp as mp

aprx_path = r'C:\xxxxxx.aprx'

#Check path
if not arcpy.Exists(aprx_path):
    print('Path not valid')
    sys.exit()

#project reference
aprx = mp.ArcGISProject(aprx_path)

#Properties
fp = aprx.filePath
print(f'File path: {fp}')

hf = aprx.homeFolder
print(f'Home Folder: {hf}')

dv = aprx.documentVersion
print(f'Document version: {dv}')

# Name project from path
def name(fp):
    name = fp.split('\\')[-1].split('.')[0]
    return name
print(f'Name project: {name(fp)}')
