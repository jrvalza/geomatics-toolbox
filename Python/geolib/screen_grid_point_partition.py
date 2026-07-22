
import random
from geolib.Screen  import Screen
from utilities.utilities import point_in_rectangle

#Init
extent = [0, 0, 800, 600]
size = 200

# 1. Callback functions

def create_grid(event):
    x_min, y_min, x_max, y_max = extent

    delta_x = x_max - x_min
    delta_y = y_max - y_min

    number_of_rows = int(delta_y / size)
    number_of_columns = int(delta_x / size)

    coordinates = []
    attributes = []

    #Grid
    for row in range (number_of_rows):

        for col in range (number_of_columns):
            x_cell_min = x_min + (col*size)
            y_cell_min = y_min + (row*size)

            cell = [[x_cell_min, y_cell_min],
                [x_cell_min+size, y_cell_min],
                [x_cell_min+size, y_cell_min+size],
                [x_cell_min, y_cell_min+size],
                [x_cell_min, y_cell_min]]

            coordinates.append(cell)
            attributes.append({'id': f'{row}-{col}'})

    screen._polylines._coordinates = coordinates
    screen._polylines._attributes= attributes

def show_coordinates(event):
    for pol, coords in enumerate(screen._polylines._coordinates):
        print(f"polilinea {pol+1}, coordenadas: {coords}")

def draw_grid (event):
    for cell in screen._polylines._coordinates:
        screen.draw_polyline(cell, colour='white')

def draw_id(event):
    for cell, id in zip(screen._polylines._coordinates, screen._polylines._attributes):
        #pixel coordinates
        x, y = cell[0][0], cell[0][1]

        # text on graphic screen
        screen.draw_text(point=[x+100,y+100], message=id['id'], colour='yellow')

def create_random_points(event):
    screen._points.random_points(1000, 0, 0, 800, 600)

def split_random_points(event):
    colors=['white', 'red', 'green', 'violet','yellow', 'blue', 'pink', 'gray', 'brown', 'gold', 'orange', 'purple']

    for rectangle in screen._polylines._coordinates:
        #Init
        x_coords=[]
        y_coords=[]
        for x, y in rectangle:
            x_coords.append(x)
            y_coords.append(y)

        #rectangle format (utilities)
        cell_rectangle = [min(x_coords),min(y_coords), max(x_coords), max(y_coords)]
        
        #random color by rectangle
        colour = random.choice(colors)
 
        #draw points in diferent colours
        for point in screen.points.coordinates:
            if point_in_rectangle(point, cell_rectangle): # utilities method
                
                screen.draw_point(point, colour=colour)

# 2. Screen()
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', create_grid)
screen.keyboard_bind('2', show_coordinates)
screen.keyboard_bind('3', draw_grid)
screen.keyboard_bind('4', draw_id)
screen.keyboard_bind('5', create_random_points)
screen.keyboard_bind('6', split_random_points)

# 4. Loop
screen.loop()
