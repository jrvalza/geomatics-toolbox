
import json
from utilities import utilities

#first 10 polylines
dictionary = utilities.read_polylines_csv('tramos', 'id_tramo', 'x', 'y', separator=',')
print(len(dictionary))
print(json.dumps(dictionary, indent=4))
