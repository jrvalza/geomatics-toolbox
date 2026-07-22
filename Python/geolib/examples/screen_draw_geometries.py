
from geolib.Screen import Screen

# 1. Callback functions
def draw_points(event):
    point = [200, 200]
    point2 = [200, 500]
    screen.draw_point(point, colour='red')
    screen.draw_point(point2, colour='cyan', size=10)

def draw_points_cloud(event):
    screen._points.random_points(100, 0, 0, 800, 600)

    for count, point in enumerate(screen.points.coordinates):
        if count %2==0:
            screen.draw_point(point, colour='red')
        else:
            screen.draw_point(point, colour='blue')
            
def draw_polyline (event):
    polyline = [[100,100], [500,100], [200,400]]
    screen.draw_polyline(polyline, thickness=10, colour='yellow')

def delete_all(event):
    screen.delete('all')

# 2. Screen()
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', draw_points)
screen.keyboard_bind('2', draw_points_cloud)
screen.keyboard_bind('3', draw_polyline)
screen.keyboard_bind('4', delete_all)

# 4. Loop
screen.loop()
