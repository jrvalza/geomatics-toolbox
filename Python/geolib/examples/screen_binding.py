
from geolib.Screen import Screen

# 1. Callback functions
def print_keyboard(event):
    print('Key 1')

def print_mouse(event):
    x, y = event.x, event.y
    print(f'left button x:{x}, y:{y}')

# 2. Screen()
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', print_keyboard) # keyboard
screen.mouse_bind('<Button-1>', print_mouse) # <Button-1>: mouse left buttom

# 4. Loop
screen.loop()
