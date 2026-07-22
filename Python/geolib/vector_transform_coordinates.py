
from geolib.Vector import Vector

dataset = Vector()

#generate 3 random points
dataset.random_points(3, -6, 25, 0, 45)

#set epsg
dataset.epsg = 4326
print(dataset)
print(dataset.coordinates)

#epsg = 4326    #WGS84
#epsg = 25830   #ETRS89 zone 30

#transform coordinates
dataset.project(25830)
print(dataset)
print(dataset.coordinates)
