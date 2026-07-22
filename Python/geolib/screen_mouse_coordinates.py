
from geolib.Screen import Screen

# 1. Callback functions
def print_mouse(event):
    x, y = event.x, event.y
    print(f'left button x:{x}, y:{y}')

def mouse_coordinates(event):
    screen.delete('text')

    # pixel coordinates
    x, y = event.x, event.y
    position = f'({x},{y})'

    # text on graphic screen
    screen.draw_text([x,y], position)

# 2. Screen()
screen = Screen()

# 3. Bindings
screen.mouse_bind('<Button-1>', print_mouse) # <Button-1>: mouse left buttom
screen.mouse_bind('<Motion>', mouse_coordinates) # <Motion>: mouse motion
screen.cursor('tcross') # X for the on-screen cursor

# 4. Loop
screen.loop()
