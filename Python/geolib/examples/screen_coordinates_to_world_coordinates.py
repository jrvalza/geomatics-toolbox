
from geolib.Screen import Screen

# 1. Callback functions
def draw_image(event):
    screen.image.read_image()
    print(screen.image)
    screen.draw_image()

def print_mouse(event):
    x, y = event.x, event.y
    print(f'left button x:{x}, y:{y}')

def world_coordinates(event):
    screen.screen_to_world()
    print(screen._points.coordinates)

# 2. Screen()
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', draw_image)
#<F9> start digitising points
#<F10> stop digitising points
screen.mouse_bind('<Button-1>', print_mouse)
screen.keyboard_bind('2', world_coordinates)
#<CTRL+F6> show points repr

# 4. Loop
screen.loop()
