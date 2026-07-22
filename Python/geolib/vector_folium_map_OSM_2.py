
from geolib.Vector import Vector

# Instance class Vector with Point geometry
dataset = Vector(geometry='point')

# 1000 random points
dataset.random_points(1000, -180, -90, 180, 90)

#===================iteration===================
# Init
rectangle = [-11.2, 35.2, 5.2, 44.3]
x_min, y_min, x_max, y_max = rectangle
coords = []
attrs = []
for count, point in enumerate(dataset.coordinates):
    x, y = point
    if (x >= x_min and x<=x_max) and (y >= y_min and y<=y_max):
        coords.append([x,y])
        attrs.append(dataset.attributes[count])

print(coords)
print('*'*50)
print(attrs)
# update attributes and coordinates
dataset._coordinates = coords
dataset._attributes = attrs

# Map OpenStreetMap
dataset.epsg = 4326 # WGS84
dataset.osm()
