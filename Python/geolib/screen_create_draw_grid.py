
from geolib.Screen import Screen

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

    #Init
    cell_id = 0

    #Grid
    for row in range (number_of_rows):
        for col in range (number_of_columns):
            x_cell_min = x_min + (col*size)
            y_cell_min = y_min + (row*size)
            cell_id += 1

            cell = [[x_cell_min, y_cell_min],
                [x_cell_min+size, y_cell_min],
                [x_cell_min+size, y_cell_min+size],
                [x_cell_min, y_cell_min+size],
                [x_cell_min, y_cell_min]]

            coordinates.append(cell)
            attributes.append({'id': cell_id})

    screen._polylines._coordinates = coordinates
    screen._polylines._attributes= attributes


def draw_grid (event):
    for cell in screen._polylines._coordinates:
        screen.draw_polyline(cell, colour='green')

# 2. Screen()
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', create_grid)
screen.keyboard_bind('2', draw_grid)

# 4. Loop
screen.loop()
