
from geolib.Screen import Screen
from utilities import utilities

# 1. Callback functions

def draw_image(event):
    screen.image.read_image()
    screen.draw_image()

def polyline(event):
    #Init
    first_point = screen._digit._coordinates[0]
    polyline = screen._digit._coordinates
    #close polyline
    polyline.append(first_point)
    #Draw polyline
    screen.draw_polyline(polyline=polyline, colour='red', thickness=3)

def convert_coordinates(event):
    screen.screen_to_world()

def area_of_rectangle(event):
    if len (screen._points._coordinates) != 5:
        print('Calculate area only for a rectangle figure')
        return

    short_side1 = utilities.segment_length([screen._points._coordinates[0], screen._points._coordinates[1]])
    short_side2 = utilities.segment_length([screen._points._coordinates[2], screen._points._coordinates[3]])

    long_side1 = utilities.segment_length([screen._points._coordinates[1], screen._points._coordinates[2]])
    long_side2 = utilities.segment_length([screen._points._coordinates[3], screen._points._coordinates[4]])

    length = (long_side1 + long_side2)/2
    width = (short_side1 + short_side2)/2
    area = length * width
    print(f'Area: {round(area/10000,2)}ha')

# 2. Screen()
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', draw_image)
screen.keyboard_bind('2', polyline)
screen.keyboard_bind('3', convert_coordinates)
screen.keyboard_bind('4', area_of_rectangle)

# 4. Loop
screen.loop()
