
import random
from geolib.Screen import Screen
from geolib.Vector import Vector

# Init
dataset = Vector()
n = 2
xmin, ymin, xmax, ymax = [0, 0, 800, 600]
min_length = 500
colours = ['red', 'violet','yellow', 'blue', 'pink', 'gray','brown', 'green', 'white', 'purple']


# 1. Callback functions
def create_random_segments(event):

    dataset.random_segments(n, xmin, ymin, xmax, ymax, min_length)
    print(dataset)
    print("*"*50)
    print("coordinates: ", dataset.coordinates)
    print("*"*50)
    print("attributes: ", dataset.attributes)

    for segment in dataset.coordinates:
        color = random.choice(colours)
        screen.draw_polyline(segment, colour=color)

# 2. Screen() instance
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', create_random_segments)

# 4. Loop
screen.loop()
