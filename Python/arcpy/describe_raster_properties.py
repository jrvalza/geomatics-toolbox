
import arcpy.da as da

raster_path = r'C:\xxxxxxx.asc'
desc = da.Describe(raster_path)

print(f"path: {desc['catalogPath']}")
print(f"Base name: {desc['baseName']}")

print(f"Width (pix): {desc['width']}")
print(f"Height (pix): {desc['height']}")
print(f"Pixel resolution: {desc['meanCellHeight']}")
print(f"Band number: {desc['bandCount']}")
print(f"Extent: {desc['extent']}")
