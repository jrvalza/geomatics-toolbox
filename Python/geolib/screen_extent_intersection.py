
from geolib.Screen import Screen
from utilities import utilities

# Init
point_1 = [50, 50, 500, 550]
point_2 = [100, 250, 750, 350]

coordinates = []
attributes = []

# 1. Callback functions
def random_point_clouds(event):
    # Init
    xmin1, ymin1, xmax1, ymax1 = point_1
    xmin2, ymin2, xmax2, ymax2 = point_2
    screen.draw_polyline([[xmin1, ymin1],
               [xmin1, ymax1],
               [xmax1, ymax1],
               [xmax1, ymin1],
               [xmin1, ymin1]])

    screen.draw_polyline([[xmin2, ymin2],
               [xmin2, ymax2],
               [xmax2, ymax2],
               [xmax2, ymin2],
               [xmin2, ymin2]])

    # Cloud 1
    screen._points.random_points(1000, xmin1, ymin1, xmax1, ymax1)
    for coord in screen.points.coordinates:
        coordinates.append(coord)
        attributes.append({'extent':1, 'color': 'red'})

    # Cloud 2
    screen._points.random_points(1000, xmin2, ymin2, xmax2, ymax2)
    for coord in screen.points.coordinates:
        coordinates.append(coord)
        attributes.append({'extent':2, 'color': 'blue'})

    screen._points._coordinates = coordinates
    screen._points._attributes = attributes

    #draw all points
    for count, point in enumerate(screen._points._coordinates):
        id_cloud = screen._points._attributes[count]['extent']
        if id_cloud == 1:
            screen.draw_point(point, colour='red')

        elif id_cloud == 2:
            screen.draw_point(point, colour='blue')

def intersect_extents(event):
    screen.delete(tag='point')
    intersect_extent = utilities.intersect_extents(point_1, point_2)
    points = []

    #Points in intersect extent
    for point in screen._points._coordinates:
        if utilities.point_in_rectangle(point, intersect_extent):
            points.append(point)

    #Draw point
    for point in points:
        screen.draw_point(point, colour='yellow')

# 2. Screen()
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', random_point_clouds)
screen.keyboard_bind('2', intersect_extents)

# 4. Loop
screen.loop()
