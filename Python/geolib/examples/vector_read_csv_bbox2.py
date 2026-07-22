
import json
from geolib.Vector import Vector

dataset = Vector()
print(dataset)

# CSV nomenclator ngbe.csv
dataset.read_csv('id', 'long_etrs89_regcan95', 'lat_etrs89_regcan95', separator=';')
dataset.epsg = 4258
print(dataset)

#get BBOX
dataset.bounding_box()
print(dataset)

print(json.dumps(dataset.coordinates[:2], indent=4))
print(json.dumps(dataset.attributes[:2], indent=4))
print(json.dumps(dataset.fields, indent=4))
