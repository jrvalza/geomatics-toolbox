
from geolib.Screen import Screen
from utilities import utilities

# Init
polyline = [[100,100],[100,500],[700,500],[700,100],[100,100]]

# 1. Callback functions
def polyline_length(event):

    result = utilities.polyline_length(polyline)
    print("Longitud total: ", result)

    #Draw polyline
    screen.draw_polyline(polyline)

# 2. Screen() instance
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', polyline_length)

# 4. Loop
screen.loop()
