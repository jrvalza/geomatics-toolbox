# geolib

A lightweight Python library with reusable utilities for handling and visualizing geospatial data.

## Features

- Raster data handling
- Vector data handling
- Coordinate transformation utilities
- Geometry visualization
- Simple drawing and screen utilities

## Installation

#### Using Conda

```bash
conda env create -f environment.yml
conda activate venv_geolib
```

## Requirements

- Python 3.10+
- Dependencies are listed in `environment.yml`.

## Basic usage

```python
from geolib.Raster import Raster
from geolib.Vector import Vector
from geolib.Screen import Screen
```

## Project structure

```text
geolib/
├── geolib/
│   ├── __init__.py
│   ├── Raster.py
│   ├── Screen.py
│   └── Vector.py
├── utilities/
│   ├── __init__.py
│   ├── utilities.py
├── examples/
│   ├── raster_read_image.py
│   ├── vector_read_csv_bbox.py
│   ├── screen_extent_intersection.py
│   └── ...
├── environment.yml
└── README.md
```

## Examples

The `examples/` directory contains example scripts demonstrating the main features of the library.
