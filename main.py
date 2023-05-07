import os
from waitress import serve
from flask_cors import CORS
from flask_restful import Api
from DbConnection.DbClass import DBClass
from werkzeug.utils import secure_filename
from ApiConnector.resources.CalcRes import CalcRes
from ApiConnector.resources.RouteRes import RouteRes
from ApiConnector.resources.FloorRes import FloorRes
from ApiConnector.resources.PlaceRes import PlaceRes
from flask import Flask, send_file, request, Response
from ApiConnector.resources.FloorsRes import FloorsRes
from ApiConnector.resources.PlacesRes import PlacesRes
from ApiConnector.resources.SensorRes import SensorRes
from ApiConnector.resources.SensorsRes import SensorsRes
from ApiConnector.resources.TerritoryRes import TerritoryRes
from ApiConnector.resources.WordPlacesRes import WordPlacesRes

dbClass = DBClass()
application = Flask(__name__)
application.secret_key = 'home position key'
application.config['SESSION_TYPE'] = 'filesystem'
application.config['MAX_CONTENT_LENGTH'] = 20 * 1000 * 1000
application.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ApiConnector/Pictures')
api = Api()
CORS(application)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
api.add_resource(SensorsRes, "/api/sensors/")
api.add_resource(CalcRes, "/api/my/position/")
api.add_resource(SensorRes, "/api/sensors/<int:sens_id>/", "/api/sensors/")
api.add_resource(TerritoryRes, "/api/territory/")
api.add_resource(FloorsRes, "/api/floor/")
api.add_resource(FloorRes, "/api/floor/", "/api/floor/<int:floor>/")
api.add_resource(PlaceRes, "/api/place/<int:place_id>/")
api.add_resource(WordPlacesRes, "/api/places/")
api.add_resource(PlacesRes, "/api/place/", "/api/place/<int:place_id>/")
api.add_resource(RouteRes, "/api/routes/")
api.init_app(app=application)


def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@application.route('/api/pictures/', methods=['POST'])
def downloadPict():
    if 'file' not in request.files:
        return {}, 400
    file = request.files['file']
    if file.filename == '':
        return {}, 400
    if file and allowedFile(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
        return {}, 200


@application.route('/api/pictures/<string:pict_name>/', methods=['GET'])
def loadPict(pict_name: str):
    filename = "ApiConnector/Pictures/" + pict_name
    parts = pict_name.split(".")
    return send_file(filename, mimetype=f'image/{parts[1]}')


@application.route('/api/floor/picture/', methods=['POST'])
def updFloorPict():
    if 'file' not in request.files:
        return {}, 400
    file = request.files['file']
    if file.filename == '':
        return {}, 400
    if file and allowedFile(file.filename):
        floorStr = request.args.get('floor')
        pict_name = dbClass.getFloorPhoto(floor=int(floorStr))
        os.remove(os.path.join(application.config['UPLOAD_FOLDER'] + "/" + pict_name))
        file.save(os.path.join(application.config['UPLOAD_FOLDER'], pict_name))
        return {}, 200
    else:
        return {}, 400


@application.route('/api/place/<string:word>/', methods=['GET'])
def getPlacesByWordPict(word: str):
    places = dbClass.getPlaceByWordJSON(substring=word)
    return Response(places, mimetype='application/json')


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=80)
    # serve(application, host="0.0.0.0", port=8080)
