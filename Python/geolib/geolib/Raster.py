
import os
import json
import tkinter
import tkinter.filedialog

class Raster():
    # Constructor
    def __init__(self):
        self._filename= None
        self._epsg = None
        self._photoimage = None
        self._world_file = None

    # Representation
    def __repr__(self):
        report = {"filename": self._filename,
                  "epsg": self._epsg,
                  "world": self._world_file
                }
        return json.dumps(report, indent=4) # String from a dictionary

    #=====================================Properties==========================================

    # (3 parts ->setter, getter y property)
    def _set_epsg(self, code):
        self._epsg = code

    def _get_epsg(self):
        return self._epsg
    epsg = property(fget=_get_epsg, fset=_set_epsg)

    def _get_shape(self):
        if self._photoimage is None:
            return
        return [self._photoimage.height(), self._photoimage.width()]
    shape = property(fget=_get_shape)

    #=READ WORLD FILE=
    def _read_world_file(self):
        # separate Filename, extension file
        image_filename, image_extension = os.path.splitext(self._filename)

        # World filename (png & gif Images)
        world_extension = image_extension[1] + image_extension[-1] + 'w' # extension 'pgw' or 'gfw
        world_filename = image_filename + '.' + world_extension

        # open file
        try:
            with open (world_filename, 'rt') as world_file:
                records = world_file.readlines()

            # convert values to float
            world_file_parameters = list(map(float, records))

            # check there are 6 parameters and save
            if len (world_file_parameters) == 6:
                self._world_file = world_file_parameters

        except:
            pass

    #==================================User methods===========================================

    def read_image (self):
        # remove tkinter window
        tkinter.Tk().withdraw()

        # Dialogue box
        filename = tkinter.filedialog.askopenfilename(
            title="Select input image file",
            filetypes=[("PNG Files", "*.png"), ("GIF Files", "*.gif")]) # optimal format for tkinter

        # We check the opening of the file
        if not filename: # exit of function
            return

        self._filename = filename
        self._photoimage = tkinter.PhotoImage(file=filename)

        #World file
        '''
        PNG image the worldfile is .PGW
        Parameters:
            1-) size pixel (longitude)
            2-) Rotation in Ortophoto is 0
            3-) Rotation in Ortophoto is 0
            4-) negative size pixel (latitude)
            5-) X coord (longitude) upper left pixel
            6-) Y coord (latitude)  upper left pixel
        '''
        # Read World file
        self._read_world_file()

        # Read projection file
