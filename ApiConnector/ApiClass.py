import os
from flask_cors import CORS
from flask_restful import Api
from DbConnection.DbClass import DBClass
from werkzeug.utils import secure_filename
from ApiConnector.resources.CalcRes import CalcRes
from ApiConnector.resources.PlaceRes import PlaceRes
from ApiConnector.resources.FloorRes import FloorRes
from flask import Flask, request, send_file, Response
from ApiConnector.resources.PlacesRes import PlacesRes
from ApiConnector.resources.FloorsRes import FloorsRes
from ApiConnector.resources.SensorRes import SensorRes
from ApiConnector.resources.SensorsRes import SensorsRes
from ApiConnector.resources.TerritoryRes import TerritoryRes


class ApiClass:
    def __init__(self):
        self.dbClass = DBClass()
        self.app = Flask(__name__)
        self.app.secret_key = 'home position key'
        self.app.config['SESSION_TYPE'] = 'filesystem'
        self.app.config['MAX_CONTENT_LENGTH'] = 20 * 1000 * 1000
        self.app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Pictures')
        self.api = Api()
        CORS(self.app)
        self.ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    def run(self):
        self.__initServe()
        self.__addRoutes()
        # self.app.run(port=80, host='192.168.100.3')
        # serve(self.app, host="0.0.0.0", port=8080)

    def __initServe(self):
        self.api.add_resource(SensorsRes, "/api/sensors/")
        self.api.add_resource(CalcRes, "/api/my/position/")
        self.api.add_resource(SensorRes, "/api/sensors/<int:sens_id>/", "/api/sensors/")
        self.api.add_resource(TerritoryRes, "/api/territory/")
        self.api.add_resource(FloorsRes, "/api/floor/")
        self.api.add_resource(FloorRes, "/api/floor/", "/api/floor/<int:floor>/")
        self.api.add_resource(PlaceRes, "/api/place/<int:place_id>/")
        self.api.add_resource(PlacesRes, "/api/place/", "/api/place/<int:place_id>/")
        self.api.init_app(app=self.app)

    # Функция проверки расширения файла
    def __allowedFile(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def __addRoutes(self):
        @self.app.route('/api/pictures/', methods=['POST'])
        def downloadPict():
            if 'file' not in request.files:
                return {}, 400
            file = request.files['file']
            if file.filename == '':
                return {}, 400
            if file and self.__allowedFile(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
                return {}, 200

        @self.app.route('/api/pictures/<string:pict_name>/', methods=['GET'])
        def loadPict(pict_name: str):
            filename = "Pictures\\" + pict_name
            parts = pict_name.split(".")
            return send_file(filename, mimetype=f'image/{parts[1]}')

        @self.app.route('/api/floor/picture/', methods=['POST'])
        def updFloorPict():
            if 'file' not in request.files:
                return {}, 400
            file = request.files['file']
            if file.filename == '':
                return {}, 400
            if file and self.__allowedFile(file.filename):
                floorStr = request.args.get('floor')
                pict_name = self.dbClass.getFloorPhoto(floor=int(floorStr))
                os.remove(os.path.join(self.app.config['UPLOAD_FOLDER'] + "/" + pict_name))
                file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], pict_name))
                return {}, 200
            else:
                return {}, 400

        @self.app.route('/api/place/<string:word>/', methods=['GET'])
        def getPlacesByWordPict(word: str):
            places = self.dbClass.getPlaceByWordJSON(substring=word)
            return Response(places, mimetype='application/json')
