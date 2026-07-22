
from geolib.Vector import Vector

dataset = Vector()

#generate 100 random points
dataset.random_points(100, -6, 25, 0, 45)

#set epsg 4326 - sysref WGS84
dataset.epsg = 4326

#mapping (html file and open browser)
dataset.osm()

print(dataset)
