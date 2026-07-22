
from geolib.Screen import Screen

# 1. Callback functions
def draw_image(event):
    screen.image.read_image()
    print(screen.image)
    #Xw = Ax + By + C -> A is the first parameter, B is the second parameter, C is the fifth parameter “X-coordinate of the upper-left corner”
    #Yw = Dx + Ey + F -> D is the third parameter, E is the fourth parameter, F is the sixth parameter “Y-coordinate of the upper-left corner”
    screen.draw_image()

# 2. Screen()
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', draw_image)

# 4. Loop
screen.loop()
