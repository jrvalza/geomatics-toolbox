
import json
from geolib.Vector import Vector

dataset = Vector()

#generate 3 random points
dataset.random_points(3, 0, 0, 180, 90)
print("fields\n", dataset.fields)

dataset.add_field('colour')

print("\nfields\n", json.dumps(dataset.fields, indent=4))

#set values: even-'blue', odd=red
for count, record in enumerate(dataset.attributes):

    if count%2 == 0:
        record['colour'] = 'blue'
    else:
        record['colour'] = 'red'

print("\nattributes\n", json.dumps(dataset.attributes, indent=4))

dataset.set_field_value(2,'colour', 'yellow')
print("\nattributes\n", json.dumps(dataset.attributes, indent=4))
