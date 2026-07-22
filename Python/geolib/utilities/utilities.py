
import pyproj
import requests
import tkinter.filedialog

def check_epsg(code):
    try:
        pyproj.CRS(code)
        return True
    except:
        return False

def copy_vector(source, target):
    target._coordinates = source._coordinates
    target._attributes = source._attributes
    target._geometry = source._geometry
    target._source = source._source
    target._format = source._format
    target._epsg = source._epsg
    target._bbox= source._bbox
    target._screen =source._screen

def point_in_rectangle(point, rectangle):
    x_min, y_min, x_max, y_max = rectangle
    x_point, y_point = point

    status = False
    if x_point > x_min and x_point < x_max and y_point > y_min and y_point < y_max:
        status = True
    return status
    
def rectangle_to_polyline(rectangle):
    x_min, y_min, x_max, y_max = rectangle
    
    polyline = [
        [x_min, y_min],
        [x_min, y_max],
        [x_max, y_max],
        [x_max, y_min],
        [x_min, y_min],
    ]
    return polyline

def merge_vectors(source, target):
    # Check empty list
    if not source:
        return

    # Check same geometry and espg code
    geometries = [vector._geometry for vector in source]
    epsgs = [vector.epsg for vector in source]

    geometry_types = set(geometries)
    epsg_types = set(epsgs)

    if len(geometry_types)==1 and len(epsg_types)==1:
        # Init
        coordinates = []
        attributes = []
        cont = 0
        for vector in source:
            for coords in vector.coordinates:
                # merge coords
                coordinates.append(coords)

                # new attributes
                attributes.append({'id':cont})
                cont += 1

        #Update target
        target._geometry = list(geometry_types)[0]
        target._coordinates = coordinates
        target._attributes = attributes
        target._epsg = list(epsg_types)[0]
    else:
        return

#segments intersection
def intersect (p_1, p_2, p_3, p_4):
    """Computes intersection betwen segment 1 (p_1-p_2) and segment 2 (p_3-p_4)"""
    x_1, y_1 = p_1
    x_2, y_2 = p_2
    x_3, y_3 = p_3
    x_4, y_4 = p_4

    # Check denominator
    d = (y_2 - y_1) * (x_4 - x_3) - (x_2 - x_1) * (y_4 - y_3)

    if d == 0:
        return None # parallel segments, no intersection

    # Numerators
    n_a = (x_1 - x_3) * (y_4 - y_3) - (y_1 - y_3) * (x_4 - x_3)
    n_b = (x_2 - x_1) * (y_3 - y_1) - (y_2 - y_1) * (x_3 - x_1)

    # Scale factors
    u_a = n_a / d
    u_b = n_b / d

    # Intersection (segment 1)
    x_intersection = x_1 + u_a * (x_2 - x_1)
    y_intersection = y_1 + u_a * (y_2 - y_1)

    # Type of intersection
    if u_a >= 0.0 and u_a <= 1.0 and u_b >= 0.0 and u_b <= 1.0:
        type_intersection = True # Two segments intersect

    elif (u_a < 0.0 or u_a > 1.0) and (u_b < 0.0 or u_b > 1.0):
        type_intersection = False # Neither of the two line segments reaches the intersection; they intersect only if you extend both lines.

    else:
        type_intersection = None # Mixed case: One of the segments does reach the intersection, but the other would need to be extended

    return [x_intersection, y_intersection, type_intersection]

def intersect_extents(extent_1, extent_2):
    #Init
    xmin1, ymin1, xmax1, ymax1 = extent_1
    xmin2, ymin2, xmax2, ymax2 = extent_2

    #Create polylines
    extent1 = [[xmin1, ymin1],
               [xmin1, ymax1],
               [xmax1, ymax1],
               [xmax1, ymin1],
               [xmin1, ymin1]]
    
    extent2 = [[xmin2, ymin2],
               [xmin2, ymax2],
               [xmax2, ymax2],
               [xmax2, ymin2],
               [xmin2, ymin2]]

    #Segments
    polyline_segments = []
    for polyline_count, polyline in enumerate([extent1, extent2]):
        for segment_count in range (1,len(polyline)):
            start = polyline[segment_count-1]
            end = polyline[segment_count]
            polyline_segments.append({'polyline': polyline_count,
                             'segment': segment_count,
                             'coordinates': [start, end]})

    #Intersections
    n_segments = len(polyline_segments)
    intersect_coordinates = []
    #intersect_attributes = []

    for i in range (n_segments):
        for j in range (i+1, n_segments):

            #Segments in same polyline
            if polyline_segments[i]['polyline'] == polyline_segments[j]['polyline']:
                continue

            #Extract segments
            p_1, p_2 = polyline_segments[i]['coordinates']
            p_3, p_4= polyline_segments[j]['coordinates']

            #Intersect
            intersection = intersect(p_1, p_2, p_3, p_4)

            if intersection is None:
                continue

            if intersection[2] is None or intersection[2] is False:
                continue

            point_intersect = [intersection[0],intersection[1]]
            intersect_coordinates.append(point_intersect)

    if len(intersect_coordinates) == 0:
        return None

    #Some points in Extension 2 fall within Extension 1
    for point in extent2:
        if point_in_rectangle(point, extent_1):
            intersect_coordinates.append(point)

    #Intersection extent
    x_coords = []
    y_coords = []
    for point in intersect_coordinates:
        x, y = point
        x_coords.append(x)
        y_coords.append(y)
    x_min = min(x_coords)
    x_max = max(x_coords)
    y_min = min(y_coords)
    y_max = max(y_coords)
    return [x_min, y_min, x_max, y_max]

def read_polylines_csv(filename, id_field, x_field, y_field, separator=','):
   
    # remove tkinter window
    tkinter.Tk().withdraw()

    # dialogue box
    filename = tkinter.filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV Files", "*.csv *.CSV")])

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

    #Init
    id_index = None
    x_index = None
    y_index = None

    # get a Indexes fields for file_name
    for field_index, field_name in enumerate(header):
        if field_name == id_field:
            id_index = field_index

        elif field_name == x_field:
            x_index = field_index

        elif field_name == y_field:
            y_index = field_index

    if id_index is None or x_index is None or y_index is None:
        # Bad parameters passed by user
        return

    wrong_records = 0
    id_tramo = []
    for record in data[1:]:
        try:
            #Split records in separate field values
            field_values = record.strip().split(separator)
            id_tramo.append(field_values[id_index])
        except:
                wrong_records += 1 # increase  number of wrong records
                continue           # jump to next record
 
    #Polylines
    polylines = {}
    a = 0
    for polyline_id in set(id_tramo):
        # Init
        for record in data[1:]:
            try:
                #Split records in separate field values
                field_values = record.strip().split(separator)
                id = field_values[id_index]

                if id == polyline_id:
                    x = float(field_values[x_index])
                    y = float(field_values[y_index])

                    #Save data
                    if polyline_id in polylines.keys():
                        polylines[polyline_id]['coordinates'].append([x,y])
                    else:
                        polylines[polyline_id] = {'coordinates':[[x,y]],
                                                  'attributes':{'id':polyline_id}}
            except:
                continue
        a += 1
        if a ==10:
            break
    return polylines

def polyline_length(polyline):

    #Init
    polyline_length = 0

    if len(polyline) == 0:
        return

    for i in range(1, len(polyline)):
        x1, y1 = polyline[i-1]
        x2, y2 = polyline[i]
        polyline_length += ((x1-x2)**2 + (y1-y2)**2)**0.5

    return float(polyline_length)

def segment_length(segment):
    #Check
    if len(segment) !=2:
        return

    x1, y1 = segment[0]
    x2, y2 = segment[1]

    #Compute length
    segment_length = ((x1-x2)**2 + (y1-y2)**2)**0.5

    return segment_length

#=====================================================================================
#=========================================API=========================================
#=====================================================================================
#valencia.opendatasoft.com/api maybe migrate to CKAN API

def vlc_opendatasoft_catalogue(version=2.1):
    #Init
    url = f'https://valencia.opendatasoft.com/api/explore/v{version}/catalog/datasets/catalogo-de-datos-abiertos/exports/json'

    #request
    response = requests.get(url)
    if response.status_code < 200 or response.status_code > 300:
        catalogue = None
    else:
        #collect data
        catalogue = response.json()
    return catalogue

def vlc_opendatasoft_find_dataset(keywork):
    catalogue = vlc_opendatasoft_catalogue()

    if catalogue is None:
        return

    # match all entrys in catalogue
    match = []
    for dataset in catalogue:
        if keywork in dataset['dataset_id']:
            match.append(dataset['dataset_id'])
    return match

def get_vlc_opendatasoft_dataset(dataset_id, version=2.1):
    url = f'https://valencia.opendatasoft.com/api/explore/v{version}/catalog/datasets/{dataset_id}/exports/geojson'

    #request
    response = requests.get(url)
    if response.status_code < 200 or response.status_code > 300:
        dataset = None
    else:
        #collect data
        dataset = response.json()
    return dataset
