
from geolib.Vector import Vector

dataset = Vector()
print(dataset)
print(dataset.epsg)

# Setter
dataset.epsg = 4326

# Getter
print(dataset.epsg)

#Read CSV  valenbisi-disponibilitat
dataset.read_csv("Numero", "geo_point_2d", "geo_point_2d", ";")
print(dataset)
