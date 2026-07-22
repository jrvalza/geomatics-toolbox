
from geolib.Vector import Vector
from utilities import utilities

# Instances Vector class
dataset_1 = Vector()
dataset_1.random_points(1000, -10, 35, 10, 45)

dataset_2 = Vector()
dataset_2.random_points(1000, 5, 40, 25, 42)

target = Vector()

print('\n\nBefore merging')
print('*'*50,'dataset-1','*'*50)
print(dataset_1)
print('*'*50,'dataset-2','*'*50)
print(dataset_2)
print('*'*50,'Target','*'*50)
print(target)

dataset_1.epsg = 4326
dataset_2.epsg = 4326

utilities.merge_vectors([dataset_1, dataset_2], target)

print('\n\nAfter merging')
print('*'*50,'dataset-1','*'*50)
print(dataset_1)
print('*'*50,'dataset-2','*'*50)
print(dataset_2)
print('*'*50,'Target','*'*50)
print(target)
