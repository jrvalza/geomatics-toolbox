
import json
from geolib.Vector import Vector

test = Vector(geometry='polyline')

print(json.dumps(test.describe_geojson(), indent=4))
print()
test.read_geojson(geometry='polyline')
print(test)
