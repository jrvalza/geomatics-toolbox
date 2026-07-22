
from geolib.Vector import Vector

dataset = Vector()
print(dataset)

#generate 200 random points
dataset.random_points(number_of_point=200, x_min=-180, y_min=-90, x_max=180, y_max=90, filename=False)

print(dataset)
