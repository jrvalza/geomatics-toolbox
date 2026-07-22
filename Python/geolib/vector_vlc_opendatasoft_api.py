
from geolib.Vector import Vector

dataset_id = 'punts-wifi-puntos-wifi'
dataset = Vector()
dataset.read_vlc_opendatasoft(dataset_id, valid_attributes=['gid', 'descripcion'])

print(dataset)
print(dataset.coordinates)
print(dataset.attributes)
