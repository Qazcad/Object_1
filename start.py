from flask import Flask
import rasterio

app = Flask(__name__)

elevation_file = 'Dem.tif'


def get_elevation(lat, lon):
    coords = ((lat, lon), (lat, lon))
    with rasterio.open(elevation_file) as src:
        vals = src.sample(coords)
        for val in vals:
            elevation = val[0]
            return elevation



@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/main/POINT(<int:coords1> <int:coords2>)')
def point(coords1, coords2):
    return ('POINT(' + str(coords1) + ' ' + str(coords2) + ' ' + str(get_elevation(coords1, coords2)) + ')')


@app.route('/main/LINESTRING(<int:coords1> <int:coords2>, <int:coords3> <int:coords4>)')
def linestring(coords1, coords2, coords3, coords4):
    return ('LINESTRING(' + str(coords1) + ' ' + str(coords2) + ' ' + str(get_elevation(coords1, coords2)) +
            ', ' + str(coords3) + ' ' + str(coords4) + ' ' + str(get_elevation(coords3, coords4)) + ')')