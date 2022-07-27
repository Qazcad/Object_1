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


@app.route('/main/POINT(<float:coords1> <float:coords2>)')
def point(coords1, coords2):
    return ('POINT(' + str(coords1) + ' ' + str(coords2) + ' ' + str(get_elevation(coords1, coords2)) + ')')


@app.route('/main/LINESTRING(<coords>)')
def linestring(coords):
    coords = coords.replace(',', '')
    mas = coords.split()
    leng = len(mas)
    if (leng % 2) != 0:
        return 'Ошибка в вводе кооринат'
    else:
        i = 0
        answer = ''
        while i < (leng - 1):
            answer = answer + str(mas[i]) + ' ' + str(mas[i + 1]) + \
                     ' ' + str(get_elevation(float(mas[i]), float(mas[i + 1]))) + ', '
            i = i + 2

        answer = answer[:-2]
        return 'LINESTRING(' + str(answer) + ')'
