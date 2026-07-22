
import os
import json
import folium
import random
import pyproj
import webbrowser
import tkinter
import tkinter.filedialog
import tkinter.messagebox
from utilities import utilities

class Vector():
    #=================================Special methods=========================================
    # Constructor
    def __init__(self, geometry = "point"):

        # Attributes
        if geometry.upper() not in ["POINT", "LINE", "POLYLINE", "POLYGON"]:
            self._geometry = None
        else:
            self._geometry = geometry

        self._source = None
        self._format = None
        self._epsg = None
        self._coordinates = []
        self._attributes = []
        self._bbox = None
        self._screen = {
            "transform": None,
            "coordinates": []
        }

    # Representation
    def __repr__(self):
        report = {"geometry": self._geometry,
                  "source": self._source,
                  "format": self._format,
                  "epsg": self._epsg,
                  "coordinates": len(self._coordinates),
                  "attributes": len(self._attributes),
                  "bbox": self._bbox,
                  "transform": self._screen["transform"]
                  }
        return json.dumps(report, indent=4) # String from a dictionary

    #=================================Protected Methods=======================================

    # (3 parts -> setter, getter and property)
    def _set_epsg(self, code):
        self._epsg = code

    def _get_epsg(self):
        return self._epsg
    epsg = property(fget=_get_epsg, fset=_set_epsg)

    def _get_coordinates(self):
        return self._coordinates
    coordinates = property(fget=_get_coordinates)

    def _get_attribute__(self):
        return self._attributes
    attributes = property(fget=_get_attribute__)

    def _get_fields(self):
        """Return fields names"""
        if len(self._attributes) > 0:
            fields = list(self._attributes[0].keys())
        else:
            fields = []
        return fields
    fields = property(fget=_get_fields)

    #=Read=
    def _read_point_xy_csv(self, header, data, id_file, xy_file, separator, xy):

        #Init
        id_index = None
        xy_index = None

        # get a Indexes fields for file_name
        for field_index, field_name in enumerate(header):

            if field_name == id_file:
                id_index = field_index

            elif field_name == xy_file:
                xy_index = field_index

        if id_index is None or xy_index is None:
            # Bad parameters passed by user
            return

        # Data processing
        for count, record in enumerate(data):

            #Init
            attributes = {}

            #Split records in separate field values
            field_values = record.strip().split(separator)

            # Assing special fields: ID, X, Y
            record_id = field_values[id_index] #ID

            if xy is True:
                x, y = list(map(float, field_values[xy_index].split(','))) # convert to float

            elif xy is False:
                y, x = list(map(float, field_values[xy_index].split(','))) # convert to float

            #Assign other fields regular attributes
            for field_index, field_value in enumerate(field_values):
                # Do not process id_field, xy_field
                if field_index == id_index or field_index ==xy_index:
                    continue

                attributes[header[field_index]] = field_value

            # Store in memory
            self._coordinates.append([x,y])
            self._attributes.append(attributes)

        #Other instance attributes
        self._format = 'csv'
        self._source = 'file'

    def _read_point_csv(self, header, data, id_file, x_file, y_file, separator):
        #Init
        id_index = None
        x_index = None
        y_index = None

        # get a Indexes fields for file_name
        for field_index, field_name in enumerate(header):

            if field_name == id_file:
                id_index = field_index

            elif field_name == x_file:
                x_index = field_index

            elif field_name == y_file:
                y_index = field_index

        if id_index is None or x_index is None or y_index is None:
            # Bad parameters passed by user
            return

        # Data processing
        wrong_records = 0
        for count, record in enumerate(data):

            #Init
            attributes = {}

            #Split records in separate field values
            field_values = record.strip().split(separator)

            # Assing special fields: ID, X, Y
            try:
                record_id = field_values[id_index] #ID

                attributes['id'] = record_id

                x = float(field_values[x_index])
                y = float(field_values[y_index])
            except:
                wrong_records += 1 # increase  number of wrong records
                continue           # jump to next record

            #Assign other fields regular attributes
            for field_index, field_value in enumerate(field_values):
                # Do not process id_field, xy_field
                if field_index == id_index or field_index ==x_index or field_index ==y_index:
                    continue

                attributes[header[field_index]] = field_value

            # Store in memory
            self._coordinates.append([x,y])
            self._attributes.append(attributes)

        if wrong_records > 0:
            tkinter.Tk().withdraw()
            tkinter.messagebox.showinfo("PROG", f"Wrong records found [{wrong_records}]")

        #Other instance attributes
        self._format = 'csv'
        self._source = 'file'
    
    def _read_geojson(self, filename, geometry):

        # geometry types of GeoJSON files
        if geometry.lower() == 'point':
            geometry = 'Point'
        
        elif geometry.lower() == 'polyline':
            geometry ='LineString'
        
        elif geometry.lower() == 'polygon':
            geometry ='Polygon'
        
        else:
            # Warning?
            return

        # Read GeoJSON
        with open(filename, 'rt') as geojson_file:
            data = json.load(geojson_file)

        # Get geometries and properties
        properties = []
        coordinates = []

        for feature in data['features']:
            feature_type = feature['geometry']['type']
            if feature_type == geometry:
                coordinates.append(feature['geometry']['coordinates'])
                properties.append(feature['properties'])

        return [coordinates, properties]
    
    def _describe_geojson(self, filename):
        with open(filename, 'r') as geojson_file:
            data = json.load(geojson_file)

        #Init
        report = dict()

        for feature in data['features']:
            feature_type = feature['geometry']['type']

            if feature_type in report.keys():
                report[feature_type] += 1
            else:
                report[feature_type] = 1

        return report
        
    #=Transformations=
    def _project_point(self, projection):
        # Init
        projected_points = []

        for coordinates in self._coordinates:
            x, y = coordinates
            x_proyected, y_projected = projection.transform(x, y)
            projected_points.append([x_proyected, y_projected])

        return projected_points

    def _project_polyline(self, projection):
        pass

    def _project_polygon(self, projection):
        pass

    #=Mapping=
    def _create_osm_point_layer(self, coordinates, attributes, colour, size):
        # Folium
        osm_layer = folium.FeatureGroup(name="osm")

        #default color and size
        if colour is None:
            colour = 'blue'
        if size is None:
            size = 4

        #layer with two parts, geometry and attributes
        for count, geometry in enumerate(coordinates):
            longitude, latitude = geometry

            #1-) Attributes
            osm_popup_text = ''
            for key, value in attributes[count].items():
                osm_popup_text += key.upper() + ': '
                osm_popup_text += str(value) + '<br>'

            #OSM Popup objetc
            osm_popup = folium.Popup(osm_popup_text, max_width=500)

            #2-) geometry
            osm_marker = folium.CircleMarker (
                location=[latitude, longitude],
                popup=osm_popup,
                radius=size,
                color=colour,
                fill=True,
                fill_color=colour,
                fill_opacity=0.4,
            )

            osm_layer.add_child(osm_marker)
        return osm_layer

    #=HTML_files=
    def _show_osm_map(self, layers):
        #Create map
        osm_map = folium.Map()

        # Adding layer to map
        for layer in layers:
            osm_map.add_child(layer)

        # zoom bbox
        osm_map.fit_bounds(osm_map.get_bounds())

        # Output fila html
        filename = 'osm.html'
        osm_map.save(filename)
        webbrowser.open(os.path.abspath(filename))

    #==================================User methods===========================================
    
    #=CSV_files=
    def read_csv(self, id_field, x_field, y_field, separator=",", xy=True):
        # remove tkinter window
        root = tkinter.Tk().withdraw()

        # dialogue box
        filename = tkinter.filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV Files", "*.csv *.CSV")]
        )

        # We check the opening of the file
        if not filename: # exit of function
            return

        # Read file contents (context manager)
        #"rt": read permissions and text type
        with open (filename, "rt", encoding="utf-8-sig") as csv_file:
            data = csv_file.readlines()

        # Header
        header = data[0].strip().split(separator)

        #Check fields exist
        if id_field not in header:
            tkinter.messagebox.showerror(
                "PROG", f"Field name not found -> [{id_field}]")
            return

        if x_field not in header:
            tkinter.messagebox.showerror(
                "PROG", f"Field name not found -> [{x_field}]")
            return

        if y_field not in header:
            tkinter.messagebox.showerror(
                "PROG", f"Field name not found -> [{y_field}]")
            return

        if x_field == y_field:
            if self._geometry == "point":
                self._read_point_xy_csv(header, data[1:], id_field, x_field, separator, xy) #xy: True -> the coordinates shall be [X,Y], xy: False -> [Y,X] 

        else:
            if self._geometry == "point":
                self._read_point_csv(header, data[1:], id_field, x_field, y_field, separator)

    #=GeoJSON_files=
    def read_geojson(self, geometry='point'):
        # Comprobation
        if geometry not in ['point', 'polyline', 'polygon']:
            return

        # remove tkinter window
        tkinter.Tk().withdraw()

        # Dialogue box
        filename = tkinter.filedialog.askopenfilename(
            title="Select GeoJSON file",
            filetypes=[("GeoJSON Files", "*.geojson *.json")])

        # We check the opening of the file
        if not filename: # exit of function
            return

        coordinates, attributes = self._read_geojson(filename, geometry)

        self._coordinates = coordinates
        self._attributes = attributes
        self._source = 'file'
        self._format = 'GeoJSON'
        self._epsg = 4326
        self._geometry = geometry.lower()
    
    def describe_geojson(self):
        # default sysref = wgs84
        # remove tkinter window
        root = tkinter.Tk().withdraw()

        # Dialogue box
        filename = tkinter.filedialog.askopenfilename(
            title="Select GeoJSON file",
            filetypes=[("GeoJSON Files", "*.geojson *.json")])

        # We check the opening of the file
        if not filename: # exit of function
            return

        return self._describe_geojson(filename)

    #=BBOX=
    def bounding_box(self):
        #Assume x, y coordinates
        if len(self._coordinates) == 0:
            #Message box??
            return

    #Points
        if self._geometry == 'point':
            #Init
            x_min, y_min = self._coordinates[0]
            x_max, y_max = self._coordinates[0]

            for point in self._coordinates:
                x, y = point

                # X coord
                if x < x_min:
                    x_min = x

                elif x > x_max:
                    x_max= x

                # Y coord
                if y < y_min:
                    y_min = y

                elif y > y_max:
                    y_max= y
            self._bbox = [x_min, y_min, x_max, y_max]

    #Polylines
        elif self._geometry == 'polyline':
            #Init
            x_min, y_min = self._coordinates[0][0]
            x_max, y_max = self._coordinates[0][0]

            for polyline in self._coordinates:
                for point in polyline:
                    x, y = point

                    # X coord
                    if x < x_min:
                        x_min = x

                    elif x > x_max:
                        x_max= x

                    # Y coord
                    if y < y_min:
                        y_min = y

                    elif y > y_max:
                        y_max= y
            self._bbox = [x_min, y_min, x_max, y_max]

    #Polygons
        elif self._geometry == 'polygon':
            #Init
            x_min, y_min = self._coordinates[0][0][0]
            x_max, y_max = self._coordinates[0][0][0]

            for polygon in self._coordinates:
                for part in polygon:
                    for point in part:
                        x, y = point

                        # X coord
                        if x < x_min:
                            x_min = x

                        elif x > x_max:
                            x_max= x

                        # Y coord
                        if y < y_min:
                            y_min = y

                        elif y > y_max:
                            y_max= y
            self._bbox = [x_min, y_min, x_max, y_max]

    #=Generate random roints=
    def random_points(self, number_of_point, x_min, y_min, x_max, y_max, filename=False):

        # Init
        delta_x = x_max - x_min
        delta_y = y_max - y_min
        coordinates = []
        attributes = []

        # random coordinates
        for point_number in range (number_of_point):
            x_random = x_min + random.random() * delta_x
            y_random = y_min + random.random() * delta_y

            coordinates.append([x_random, y_random])
            attributes.append({"id":point_number})

        # Instance attributes
        self._geometry = 'point'
        self._source = 'random'
        self._format = 'list'
        self._coordinates = coordinates
        self._attributes = attributes

        #Output CSV
        if filename:
            tkinter.Tk().withdraw()
            filename = tkinter.filedialog.asksaveasfilename(title="Select output CSV file", filetypes= [('CSV files', '*.csv *.CSV')])

            if filename == '':
                return

            # add csv extension
            if not filename.endswith('.csv'):
                filename += '.csv'

            with open (filename, 'wt') as csv_file:
                csv_file.write('id,x,y\n')

                for count, point in enumerate(coordinates):
                    x, y = point
                    csv_file.write(f'{count},{x},{y}\n') # write data

    #=Generate random segments of polylines=
    def random_segments(self, number_of_points, x_min, y_min, x_max, y_max, min_length=None):
        #1-)
        segments_coordinates = []
        segments_attributes = []

        #2-)
        id = 0
        while True :
            
            self.random_points(2, x_min, y_min, x_max, y_max)
        
            if min_length is None:
                segments_coordinates.append(self.coordinates)
                segments_attributes.append({'id':id})
                id += 1

            elif min_length is not None:
                # Calculate segment length
                x1, y1 = self.coordinates[0]
                x2, y2 = self.coordinates[1]
                segment_length = ((x1-x2)**2 + (y1-y2)**2)**0.5

                if float(segment_length) >= float(min_length):
                    segments_coordinates.append(self.coordinates)
                    segments_attributes.append({'id':id})
                    id += 1

            if id == number_of_points:
                break
        
        self._geometry = 'polyline'
        self._source = 'random'
        self._format = 'list'
        self._coordinates = segments_coordinates
        self._attributes = segments_attributes

    #=Add field to attributes table=
    def add_field(self, field_name, field_value=None):

        # field id forbidden
        if field_name == 'id':
            return

        # without geographical entities there are no attributes
        if len(self._coordinates)==0:
            return

        if field_name in self.fields:
            # Overwrite or not overwrite?
            # Warning
            pass

        # Write record
        for record in self._attributes:
            record[field_name] = field_value

    #=Add values to new field on attributes table=
    def set_field_value(self, record_number, field_name, field_value):

        # field id forbidden
        if field_name == 'id':
            return

        # without geographical entities there are no attributes
        if len(self._attributes) == 0:
                return

        try:
            self._attributes[record_number][field_name] = field_value
        except:
            return

    #=projecting geographical entities=
    def project(self, target_epsg):

        # EPSG Origin: self._epsg
        # EPSG destination: target_epsg

        # Comprobations
        if self._epsg == None:
            tkinter.Tk().withdraw()
            tkinter.messagebox.showerror('PROG', 'Unknown source EPSG code' )
            return

        if self._epsg == target_epsg:
            return

        try:
            source_crs = pyproj.CRS.from_epsg(self._epsg)
        except:
            tkinter.Tk().withdraw()
            tkinter.messagebox.showerror('PROG', 'Unknown source EPSG code' )
            return

        try:
            target_crs = pyproj.CRS.from_epsg(target_epsg)
        except:
            tkinter.Tk().withdraw()
            tkinter.messagebox.showerror('PROG', 'Unknown target EPSG code' )
            return

        #Transformer
        projection = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True) #always_xy=True -> x:longitud, y:latitud. always_xy=False -> x:latitud, y:longitud

        #Transformations
        if self._geometry =='point':
            projected = self._project_point(projection)


        elif self._geometry =='polyline':
            # Hacer luego
            #projected = self._project_polyline(projection)
            pass

        elif self._geometry =='polygon':
            #Hacer luego
            #projected = self._project_polygon(projection)
            pass

    # Update properties
        self._coordinates = projected
        self._epsg = target_epsg

    #=Mapping=
    def osm (self, colour=None, size=None):
    # Comprobations
        if len(self._coordinates) == 0:
            return

        #4326 or 4258 synonyms
        if self._epsg == 4326 or self._epsg == 4258:
            # Not transform
            transform = None

        elif self._epsg ==None:
            return

        else:
            # Hacer luego
            pass

    #Geometrys
        if self._geometry == 'point':

            if transform == None:# Not transform, same coordinates
                coordinates_4326 = self._coordinates
            else:
                # Transform
                coordinates_4326 = None

            # Layers
            osm_layer = self._create_osm_point_layer(coordinates_4326, self._attributes, colour, size)

        if self._geometry == 'polyline':
            # Hacer luego
            pass
        if self._geometry == 'polygon':
            # Hacer luego
            pass

        self._show_osm_map([osm_layer])
        #[osm_layer] = list of Folium layers

    #=GeoJSON from vlc opendatasoft=
    def read_vlc_opendatasoft(self, dataset_id, version=2.1, valid_attributes=None):
        #Get dataset from opendatasoft server
        dataset = utilities.get_vlc_opendatasoft_dataset(dataset_id, version=version)

        # Initial check
        if dataset is None:
            #Warning
            return

        #Extract information from GeoJSON dictionary
        #Init
        coordinates = []
        attributes = []
        for feature in dataset['features']:

            #Check geometry types match
            if feature['geometry']['type'].lower() != self._geometry:
                continue

            coordinates.append(feature['geometry']['coordinates'])

            #Discuss attributes
            if valid_attributes is None: #All from source attributes
                attributes.append(feature['properties'])

            else: #Only specific attributes
                feature_attribute_names = list(feature['properties'].keys())

                feature_attributes = {}

                for attribute_name in valid_attributes:
                    if attribute_name in feature_attribute_names:
                        attribute_value = feature['properties'][attribute_name]
                        feature_attributes[attribute_name] = attribute_value

                attributes.append(feature_attributes)

        #Update instance attributes
        self._coordinates = coordinates
        self._attributes = attributes
        self._source = 'vlc_opendatasoft'
        self._format = 'GeoJSON'
        self._epsg = 4326
