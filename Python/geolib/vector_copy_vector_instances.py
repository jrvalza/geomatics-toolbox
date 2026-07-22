
from geolib.Vector import Vector
from utilities import utilities

# Instances Vector class
source = Vector()
source.random_points(500, 0, 0, 800, 600)
target = Vector('point')

print('\n\nBefore copy')
print('*'*50,'Source','*'*50)
print(source)
print('*'*50,'Target','*'*50)
print(target)

utilities.copy_vector(source, target)

source.epsg = 4326

print('\n\nAfter copy')
print('*'*50,'Source','*'*50)
print(source)
print('*'*50,'Target','*'*50)
print(target)
