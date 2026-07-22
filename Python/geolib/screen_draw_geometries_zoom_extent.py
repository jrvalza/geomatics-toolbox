
from geolib.Screen import Screen

# 1. Callback functions
def load_polylines_geojson(event):
    screen.polylines.read_geojson(geometry='polyline')

def draw_polylines(event):
    if len(screen.polylines.coordinates) == 0:
        return
    screen.draw_vector_polylines()

# 2. Screen()
screen = Screen()

# 3. Bindings
screen.keyboard_bind('1', load_polylines_geojson)
# <Control-F7> Polylines repr
# <Shift-F9>  zoom extent
screen.keyboard_bind('2', draw_polylines)

# 4. Loop
screen.loop()
