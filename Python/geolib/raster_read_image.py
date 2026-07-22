
from geolib.Raster import Raster

raster = Raster()
print(raster)
print(raster.shape)

raster.read_image()

print('*'*100)

print(raster)
print(raster.shape)
