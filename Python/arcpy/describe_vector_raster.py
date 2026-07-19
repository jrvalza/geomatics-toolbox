
import arcpy.da as da

shp_path = r'C:\xxxxxxx.shp'

#arcpy.Describe()
# desc = arcpy.Describe(shp_path)
# if hasattr(desc, 'name'):
#     print(desc.name)

#arcpy.da.Describe() -->da: data access
desc = da.Describe(shp_path)

for key, value in desc.items():
    print(f'KEY:  {key}, VALUE:  {value}')

print("="*20)

raster_path = r'C:\xxxxxxx.asc'
desc = da.Describe(raster_path)

for key, value in desc.items():
    print(f'KEY:  {key}, VALUE:  {value}')

