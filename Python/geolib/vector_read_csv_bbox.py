
import json
from geolib.Vector import Vector

dataset = Vector()
print(dataset)

# read CSV  valenbisi-disponibilitat
dataset.read_csv('Numero', 'geo_point_2d', 'geo_point_2d',separator=';', xy=False)
dataset.epsg = 4326
print(dataset)

dataset.bounding_box()
print(dataset)

print(json.dumps(dataset.coordinates[:2], indent=4))
print(json.dumps(dataset.attributes[:2], indent=4))
print(json.dumps(dataset.fields, indent=4))
