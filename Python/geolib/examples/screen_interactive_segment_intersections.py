
import random
from geolib.Screen import Screen
from geolib.Vector import Vector
from utilities import utilities

# Global init
p_1 = Vector()
p_2 = Vector()

cell0 = [0, 0, 400, 200]
cell1 = [400, 0, 800, 200]
cell2 = [0, 200, 400, 400]
cell3 = [400, 200, 800, 400]
cell4 = [0, 400, 400, 600]
cell5 = [400, 400, 800, 600]
cells = [cell0, cell1, cell2, cell3, cell4, cell5]

# 1. Callback functions
def reset(event):

    screen.delete('all')

    screen._points._coordinates = []
    screen._points._attributes = []

    screen._polylines._coordinates = []
    screen._polylines._attributes = []

def draw_cells(event):
    for cell in cells:
        screen.draw_polyline(
            utilities.rectangle_to_polyline(cell),
            thickness=3, colour='gray', tag='cell'
            )

def delete_cells(event):
    screen.delete(tag='cell')

def random_segments(event):
    reset(None)

    coordinates = []
    attributes = []

    # Segment 0
    p_1.random_points(1, *cell0)
    p_2.random_points(1, *cell4)
    
    start = p_1.coordinates[0]
    end = p_2.coordinates[0]
    coordinates.append([start, end])
    attributes.append({'id': 0, 'colour':'cyan'})

    # Segment 1
    p_1.random_points(1, *cell1)
    p_2.random_points(1, *cell5)
    
    start = p_1.coordinates[0]
    end = p_2.coordinates[0]
    coordinates.append([start, end])
    attributes.append({'id': 1, 'colour':'red'})

    # Segment 2
    p_1.random_points(1, *cell0)
    p_2.random_points(1, *cell5)
    
    start = p_1.coordinates[0]
    end = p_2.coordinates[0]
    coordinates.append([start, end])
    attributes.append({'id': 2, 'colour':'green'})

    # Segment 3
    p_1.random_points(1, *cell1)
    p_2.random_points(1, *cell4)
    
    start = p_1.coordinates[0]
    end = p_2.coordinates[0]
    coordinates.append([start, end])
    attributes.append({'id': 3, 'colour':'violet'})

    #Save segments in memory
    screen._polylines._coordinates = coordinates
    screen.polylines._attributes = attributes

    # Draw segments
    for count, segment in enumerate(screen._polylines._coordinates):
        screen.draw_polyline(segment, colour=screen._polylines._attributes[count]['colour'], tag='segment')

def other_segment (event):
    segment = [[50, 300], [750, 300]]
    colour = 'white'
    screen.draw_polyline(segment, thickness=3, colour=colour, tag='segment')
    
    screen._polylines._coordinates.append(segment)
    screen._polylines._attributes.append({'id':4, 'colour':colour})

def intersections(event):
    #Intersections
    intersect_coordinates = []
    intersect_attributes = []
    count = 0

    p_1, p_2 = screen._polylines._coordinates[-1]

    for i in range(len(screen._polylines._coordinates)-1):
        
        p_3, p_4 = screen._polylines._coordinates[i]

        #Intersect
        intersection = utilities.intersect(p_1, p_2, p_3, p_4)

        #Save info
        if intersection[2]: #Only true intersections
            intersect_coordinates.append([intersection[0],intersection[1]])
            intersect_attributes.append({'id': count, 'type': intersection[2]})
            count+=1

    screen._points._coordinates = intersect_coordinates
    screen._points._attributes = intersect_attributes

    #Draw interseccion
    for count, point in enumerate(screen._points.coordinates):
        attribute = screen._points.attributes[count]

        if attribute['type']:
            screen.draw_point(point, colour='khaki', size=6, tag='point')

def split_diferent_color (event):
    p_init = screen._polylines.coordinates[4][0]
    p_end = screen._polylines.coordinates[4][1]

    #Split segment in 4 segments
    polyline_segments = []
    for segment_count in range (1,len(screen._points.coordinates)):

        coords = sorted(screen._points.coordinates) #sorted by xCoord
        start = coords[segment_count-1]
        end = coords[segment_count]

        if segment_count == 1:
            polyline_segments.append({'segment': segment_count-1, 'coordinates': [p_init, start]})

        polyline_segments.append({'segment': segment_count, 'coordinates': [start, end]})

        if segment_count == (len(screen._points.coordinates)-1):
            polyline_segments.append({'segment': segment_count+1, 'coordinates': [end, p_end]})

    # clear screen
    screen.delete('segment')
    #screen.delete('point')
    
    #Draw segments
    colours = ['red', 'violet','yellow', 'blue', 'green', 'gray','brown', 'orange', 'purple']
    for segment in polyline_segments:
        colour = random.choice(colours)
        screen.draw_polyline(segment['coordinates'], thickness=4, colour=colour, tag='segment')
    
    #draw points again    
    for point in screen._points.coordinates:    
        screen.draw_point(point, colour='khaki', size=6, tag='point')

# 2. Screen() instance
screen = Screen()

# 3. Bindings
screen.keyboard_bind('<Escape>', reset)
screen.keyboard_bind('1', draw_cells)
screen.keyboard_bind('2', delete_cells)
screen.keyboard_bind('3', random_segments)
screen.keyboard_bind('4', other_segment)
screen.keyboard_bind('5', intersections)
screen.keyboard_bind('6', split_diferent_color)

# 4. Loop
screen.loop()
