
import json
from geolib.Vector import Vector
from utilities import utilities

vector = Vector()
print(vector)

n = 5
xmin, ymin, xmax, ymax = [0, 0, 800, 600]
vector.random_segments(n, xmin, ymin, xmax, ymax)

for count, segment in enumerate(vector.coordinates):
    #compute lengths
    lenght = utilities.segment_length(segment)
    #store
    vector.attributes[count]['length']=lenght

print(vector)
print(json.dumps(vector.attributes, indent=4))

for count, lenght in enumerate(vector.attributes):
    print(f"segment {count}, length: {lenght['length']}")
