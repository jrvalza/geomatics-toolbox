
import tkinter
from geolib.Raster import Raster
from geolib.Vector import Vector
from utilities import utilities

class Screen():
    # Constructor
    def __init__(self, rows=600, columns=800, background='black'):

        self._columns = columns
        self._rows = rows
        self._root = tkinter.Tk()
        self._root.title('PROG')
        self._root.resizable(False, False)
        self._canvas = tkinter.Canvas(
            self._root, width=self._columns, height=self._rows, bg=background,
            borderwidth = 0, highlightthickness = 0
        )
        self._canvas.pack()

    #=====================System bindings=====================

        self._root.bind('<F1>', self._help)
        ##self._root.bind('<F2>', self._state_of_the_app)
        self._root.bind('<F9>', self._start_digit)
        self._root.bind('<F10>', self._stop_digit)
        self._root.bind('<F11>', self._digit_repr)
        self._root.bind('<F12>', self._digit_out)

        self._root.bind('<Shift-F5>', self._image_epsg)
        self._root.bind('<Shift-F6>', self._points_epsg)
        self._root.bind('<Shift-F7>', self._polylines_epsg)
        self._root.bind('<Shift-F8>', self._polygons_epsg)
        self._root.bind('<Shift-F9>', self.zoom_extent)

        self._root.bind('<Control-F6>', self._points_repr)
        self._root.bind('<Control-F7>', self._polylines_repr)
        self._root.bind('<Control-F8>', self._polygons_repr)
        self._root.bind('<Control-F9>', self._digit_repr)

    #=====================Datasets=====================

        self._digit = Vector(geometry='point')
        self._points = Vector(geometry='point')
        self._polylines = Vector(geometry='polyline')
        self._polygons = Vector(geometry='polygon')
        self._image = Raster()

    #=====================Properties=====================

    def _get_digit(self):
        return self._digit
    digit = property(fget=_get_digit)

    def _get_points(self):
        return self._points
    points = property(fget=_get_points)

    def _get_polylines(self):
        return self._polylines
    polylines = property(fget=_get_polylines)

    def _get_polygons(self):
        return self._polygons
    polygons = property(fget=_get_polygons)

    def _get_image(self):
        return self._image
    image = property(fget=_get_image)

    #=====================Protected methods=====================

    def _help(self, event):

        help_text = 'F1: Help\n\n'
        help_text += 'F5: Read image\n'
        help_text += 'F6: Read points\n'
        help_text += 'F7: Read polylines\n'
        help_text += 'F8: Read polygons\n\n'
        help_text += 'F9: Start digitising points\n'
        help_text += 'F10: Stop digitising points\n'
        help_text += 'F11: Digit coordinates and attributes\n'

        help_text += 'Shift-F5: Image EPSG code\n'
        help_text += 'Shift-F6: Points EPSG code\n'
        help_text += 'Shift-F7: Polylines EPSG code\n'
        help_text += 'Shift-F8: Polygons EPSG code\n\n'

        help_text += 'Control-F2: Clear screen\n\n'
        help_text += 'Control-F5: Print image properties\n'
        help_text += 'Control-F6: Print points properties\n'
        help_text += 'Control-F7: Print polylines properties\n'
        help_text += 'Control-F8: Print polygons properties\n'
        print(help_text)

    def _start_digit(self, event):
        self._root.bind('<Button-1>', self._get_point)
        self.cursor('tcross')

    def _stop_digit(self, event):
        self._root.unbind('<Button-1>')
        self.cursor()

    def _get_point(self, event):
        if self._digit._source is None:
            self._digit._source = 'digit'

        point = [event.x, event.y]
        count = len(self._digit._coordinates)
        self._digit._coordinates.append(point)
        self._digit._attributes.append({'id': count})

        self.draw_point(point)

    def _image_epsg(self, event):

        epsg = tkinter.simpledialog.askinteger(title='PROG', prompt='Image EPSG code')

        if epsg is None:
            return

        if utilities.check_epsg(epsg) is False:
            return

        self._image.epsg = epsg

    def _points_epsg(self, event):

        epsg = tkinter.simpledialog.askinteger(title='PROG', prompt='Points EPSG code')

        if epsg is None:
            return

        if utilities.check_epsg(epsg) is False:
            return

        self._points.epsg = epsg

    def _polylines_epsg(self, event):

        epsg = tkinter.simpledialog.askinteger(title='PROG', prompt='Polylines EPSG code')

        if epsg is None:
            return

        if utilities.check_epsg(epsg) is False:
            return

        self._polylines.epsg = epsg

    def _polygons_epsg(self, event):

        epsg = tkinter.simpledialog.askinteger(title='PROG', prompt='Polygons EPSG code')

        if epsg is None:
            return

        if utilities.check_epsg(epsg) is False:
            return

        self._polygons.epsg = epsg

    def _digit_repr(self, event):
        print(self._digit)

    def _points_repr(self, event):
        print(self._points)

    def _polylines_repr(self, event):
        print(self._polylines)

    def _polygons_repr(self, event):
        print(self._polygons)

    def _digit_out(self, event):

        for count, point in enumerate(self._digit._coordinates):
            attributes = self._digit._attributes[count]
            print(point, attributes)

    def _draw_single_point(self, point, size, colour, tag):
        """Draws a single point on the Screen() canvas"""
        x, y = point
        x_min = x - size
        y_min = y - size
        x_max = x + size
        y_max = y + size
        self._canvas.create_rectangle(x_min, y_min, x_max, y_max, fill=colour, tag=tag)

    def _draw_single_polyline(self, polyline, thickness, colour, tag):
        """Draws a single polyline on the Screen() canvas"""
        self._canvas.create_line(polyline, fill=colour, width=thickness, tag=tag)

    def _draw_single_polygon(self, polygon, size, colour, tag, trans):
        """Draws a single polygon on the Screen() canvas"""
        pass

    def _zoom_extent(self, k_0=0.95):

        # Comprobations
        if len(self._points.coordinates) == 0 and \
           len(self._polylines.coordinates) == 0 and \
           len(self._polygons.coordinates) == 0:
            # Warning ?
            return

        # Source bounding box
        bounding_boxes = [] # 3 types of geometries

        if self._points._bbox is None:
            self._points.bounding_box()

        if self._points._bbox is not None:
            bounding_boxes.append(self._points._bbox)

        if self._polylines._bbox is None:
            self._polylines.bounding_box()

        if self._polylines._bbox is not None:
            bounding_boxes.append(self._polylines._bbox)

        if self._polygons._bbox is None:
            self._polygons.bounding_box()

        if self._polygons._bbox is not None:
            bounding_boxes.append(self._polygons._bbox)

        #TRANSFORMATION

        # World extent (geographical coordinates)
        if len(bounding_boxes) == 1:
            xw_min, yw_min, xw_max, yw_max = bounding_boxes[0]

        else:
            #xw_min, yw_min, xw_max, yw_max = utilities.merge_bounding_boxes(bounding_boxes)
            pass

        # Screen extent (in pixel coordinates)
        xs_min, ys_min, xs_max, ys_max = [0, 0, self._columns, self._rows]

        # Increments (in world and screen)
        delta_xw = xw_max - xw_min
        delta_yw = yw_max - yw_min

        delta_xs = xs_max - xs_min
        delta_ys = ys_max - ys_min

        # Scale factor (x and y factors)
        k_1 = delta_xs / delta_xw
        k_2 = delta_ys / delta_yw
        k = min(k_1, k_2) * k_0 # k_0 is a reduction for padding screen

        # Translation in world space
        tx_world = 0.5*(xw_min + xw_max) # center point in X BBOX world space
        ty_world = 0.5*(yw_min + yw_max) # center point in Y BBOX world space

        #Scale to screen space
        tx_world *= k
        ty_world *= k

        # translation in screen space
        tx_screen = 0.5*(xs_min + xs_max) # center point in X BBOX screen space
        ty_screen = 0.5*(ys_min + ys_max) # center point in Y BBOX screen space

        # Global translation
        tx = -tx_world + tx_screen
        ty = -ty_world - ty_screen # coord Y incremento to south direction

        # Update screen() instance
        self._points._screen['transform'] = [k, tx, ty] # scale factor, translation x and translation y
        self._polylines._screen['transform'] = [k, tx, ty]
        self._polygons._screen['transform'] = [k, tx, ty]

    def _transform_polyline(self, polyline):
        #Get transform parameter
        k, tx, ty = self._polylines._screen['transform']

        #Init
        transformed_polyline = []

        for point in polyline:
            x, y = point
            x_screen = k*x + tx
            y_screen = -(k*y + ty)
            transformed_polyline.append([x_screen,y_screen])

        return transformed_polyline

    def _screen_to_world (self, x, y, affine):
        #Init
        a, d, b, e, c, f = affine

        #Affine transformation
        x_world = (a*x) + (b*y) + c
        y_world = (d*x) + (e*y) + f
        return [x_world, y_world]
    
    #=====================User Screen() methods=====================

    def loop(self):
        self._root.mainloop()

    def keyboard_bind(self, event, function):
        self._root.bind(event, function)

    def mouse_bind(self, event, function):
        self._canvas.bind(event, function)

    def cursor(self, shape='left_ptr'):
        self._canvas.config(cursor=shape)

    def delete(self, tag):
        self._canvas.delete(tag)

    def clear(self):
        self._canvas.delete('all')
        self._digit.reset()
        self._points.reset()
        self._polylines.reset()
        self._polygons.reset()

        #self._image.reset()

    #=====================User graphical methods=====================

    def add_vector(self, vector):
        if type(vector).__name__ != 'Vector':
            return
        if vector.geometry == 'point':
            self._points = vector

    def draw_point(self, point, size=3, colour='white', tag='point'):
        """Draws a single point on the Screen() canvas"""
        self._draw_single_point(point, size, colour, tag)

    def draw_polyline(self, polyline, thickness=2, colour='white', tag='polyline'):
        """Draws a single polyline on the Screen() canvas"""
        self._draw_single_polyline(polyline, thickness, colour, tag)

    def draw_polygon(self, polygon, size=3, colour='white', tag='polygon', trans=None):
        """Draws a single polygon on the Screen() canvas"""
        self._draw_single_polygon(self, polygon, size, colour, tag, trans)

    def draw_text(self, point, message, colour='white', tag='text'):
        self._canvas.create_text(
            *point, text=message, anchor='sw', fill=colour, tag=tag
        )

    def draw_vector(self, geometry='point', screen=False):
        if geometry == 'point':
            if self._points is None:
                return

    def zoom_extent(self, event):
        self._zoom_extent()

    def draw_vector_polylines(self):
        '''
        Draw Polylines on the screen with this sequence:
        1-) Using world file (only when Raster load)
        2-) Using zoom extent
        3-) Raw coordinates (file)
        '''
        #Comprobations
        if len(self._polylines.coordinates) == 0:
            # Warning??
            return

        #================================================
        #================Using world file================
        #================================================
        if self._image._photoimage is not None:
            print("World file")

        #================================================
        #================Using zoom extent===============
        #================================================
        elif self._polylines._screen['transform'] is not None:

            for polyline in self._polylines.coordinates:
                #1. Transform polyline from world to screen coordinates
                transformed_polyline = self._transform_polyline(polyline)

                #2. Draw screen coordinates
                self.draw_polyline(transformed_polyline)

        #================================================
        #==============Using raw coordinates=============
        #================================================
        else:
            print("Raw Coordinates")

    def draw_image(self):
        global image # Init None
        image = self._image._photoimage # Tkinter image format

        if image is None:
            # Warning
            return

        self._canvas.create_image(0, 0, image=image, anchor='nw') #insert image in (0,0) upper left corner. anchor point nw to (0,0)

    def screen_to_world(self):
        """Transforms digit points in screen coordinates to world coordinates"""
        if self._image._world_file is None:
            return

        # Values (affine transform) from file WoldFile
        a, d, b, e, c, f = self._image._world_file
        affine = [a, d, b, e, c, f]

        coordinates = []
        attributes = []

        #Affine transformation
        for count, point in enumerate(self._digit.coordinates):
            x, y = point
            x_world, y_world = self._screen_to_world(x, y, affine)

            #Save data in lists
            coordinates.append([x_world, y_world])
            attributes.append({'id':count})

        #Save data in memory
        self._points._coordinates = coordinates
        self._points._attributes = attributes
