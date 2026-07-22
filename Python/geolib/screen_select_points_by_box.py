
from geolib.Screen import Screen

# 1. Callback functions

def draw_points_cloud(event):
    screen.points.random_points(500, 0, 0, 800, 600)
    for point in screen.points.coordinates:
        screen.draw_point(point, colour='pink')

def draw_box(event):
    # There are 2 digitalized points
    if len(screen.digit.coordinates) !=2:
        return
    x_0, y_0 = screen.digit.coordinates[0]
    x_1, y_1 = screen.digit.coordinates[1]

    x_min = min(x_0, x_1)
    y_min = min(y_0, y_1)
    x_max = max(x_0, x_1)
    y_max = max(y_0, y_1)

    box = [[x_min, y_min],
           [x_min, y_max],
           [x_max, y_max],
           [x_max, y_min],
           [x_min, y_min]
           ]

    screen._polylines._coordinates.append(box)
    screen._polylines._attributes.append({'id':0})
    screen.draw_polyline(screen.polylines.coordinates, colour='red')

def update_points(event):
    screen.delete('point')
    if len(screen.polylines.coordinates) ==0:
        return

    # BBox
    x_min, y_min = screen.polylines.coordinates[0][0]
    x_max, y_max = screen.polylines.coordinates[0][0]

    for point in screen.polylines.coordinates[0]:
        x, y = point
        # X coord
        if x < x_min:
            x_min = x

        elif x > x_max:
            x_max= x
        # Y coord
        if y < y_min:
            y_min = y

        elif y > y_max:
            y_max= y

    for point in screen.points.coordinates:
        x, y = point
        if (x >= x_min and x<=x_max) and (y >= y_min and y<=y_max):
            continue
        else:
            # Draw Points
            screen.draw_point([x,y], colour='green')

    #Draw polyline
    screen.draw_polyline(screen.polylines.coordinates, colour='red')

# 2. Screen()
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', draw_points_cloud)
# root.bind <F9> start digit
# root.bind <F10> stop digit)
screen.keyboard_bind('2', draw_box)
screen.keyboard_bind('3', update_points)

# 4. Loop
screen.loop()
