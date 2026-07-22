
from geolib.Screen import Screen
from utilities import utilities

#points
p_1 = [600, 588]
p_2 = [600, 56]
p_3 = [614, 539]
p_4 = [150, 308]
p_5 = [271, 56]
p_6 = [593, 210]
p_7 = [440, 462]
p_8 = [502, 329]
p_9 = [590, 371]

#Polylines a, b and c are defined as follows:
a = [p_1, p_2]
b = [p_3, p_4, p_5, p_6]
c = [p_7, p_8, p_9]

# 1. Callback functions
def Store_polylines(event):
    polylines = [a,b,c]
    attributes = [{'id':'a'}, {'id':'b'}, {'id':'c'}]

    for count, polyline in enumerate(polylines):
        screen._polylines._coordinates.append(polyline)
        screen._polylines._attributes.append(attributes[count])
    print('Polylines added')

def Draw_polylines(event):
    for polyline in screen._polylines.coordinates:
        screen.draw_polyline(polyline)
    print('Drawn polylines')

def Intersect_polyline (event):
    polyline_segments = []
    for polyline_count, polyline in enumerate(screen._polylines.coordinates):
        for segment_count in range (1,len(polyline)):
            start = polyline[segment_count-1]
            end = polyline[segment_count]
            polyline_segments.append({'polyline': polyline_count,
                             'segment': segment_count,
                             'coordinates': [start, end]})

    #Intersections
    n_segments = len(polyline_segments)
    intersect_coordinates = []
    intersect_attributes = []
    count = 0

    for i in range (n_segments):
        for j in range (i+1, n_segments):

            #Segments in same polyline
            if polyline_segments[i]['polyline'] == polyline_segments[j]['polyline']:
                continue

            count += 1

            #Extract segments
            p_1, p_2 = polyline_segments[i]['coordinates']
            p_3, p_4= polyline_segments[j]['coordinates']

            #Intersect
            intersection = utilities.intersect(p_1, p_2, p_3, p_4)

            #Save info
            int_coordinates = [intersection[0],intersection[1]]
            int_attributes = {'id': count,
                              'type': intersection[2]}

            intersect_coordinates.append(int_coordinates)
            intersect_attributes.append(int_attributes)

    screen._points._coordinates = intersect_coordinates
    screen._points._attributes = intersect_attributes
    print('Intersections stores in memory')

def Draw_intersections (event):
    for count, point in enumerate(screen._points.coordinates):
        attribute = screen._points.attributes[count]

        if attribute['type'] is True:
            screen.draw_point(point, colour='cyan')

        if attribute['type'] is None:
            screen.draw_point(point, colour='red')

# 2. Screen()
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', Store_polylines)
screen.keyboard_bind('2', Draw_polylines)
screen.keyboard_bind('3', Intersect_polyline)
screen.keyboard_bind('4', Draw_intersections)

# 4. Loop
screen.loop()
