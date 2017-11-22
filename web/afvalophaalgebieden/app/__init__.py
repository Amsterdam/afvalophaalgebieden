import logging

from flask import Flask, request, views, jsonify, abort, Response
from flask.ext.cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_swagger import swagger
from geoalchemy2.elements import WKTElement

from pyproj import Proj, transform

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

from . import config

application = Flask(__name__)
log_handler = logging.StreamHandler()


application.config.from_object(config)
application.logger.addHandler(log_handler)

CORS(app=application, send_wildcard=True)

db = SQLAlchemy(application)

# vreemde locatie, maar moet ná het definieren van application
from . import models


@application.errorhandler(400)
def custom400(error):
    log.debug(error)
    response = jsonify({
        'message': error.description,
        'example_rd_x_y': "https://api.data.amsterdam.nl/afvalophaalgebieden/search/?x=120737&y=486850",
        'example_lon_lat': "https://api.data.amsterdam.nl/afvalophaalgebieden/search/?lat=52.368779124226194&lon=4.896084471070842"
    })
    response.status_code = 200
    return response


class SearchView(views.View):
    tables = ['grofvuil', 'huisvuil']

    methods = ['GET']

    def get(self):
        """
        Query for garbage collection days for the specified address (x/y or lat/lon)
        ---
        description:
            - "Returns the garbage collection days for the specified address (x/y or lat/lon)"
        tags:
            - "afvalophaalgebieden"
        produces:
            - "application/json"
        parameters:
            -
                name: "x"
                in: "query"
                description: "x-coordinate of address"
                required: false
                type: "string"
            -
                name: "y"
                in: "query"
                description: "y-coordinate of address"
                required: false
                type: "string"
            -
                name: "lat"
                in: "query"
                description: "latitude of address"
                required: false
                type: "string"
                default: "52.368779124226194"
            -
                name: "lon"
                in: "query"
                description: "longitude of address"
                required: false
                type: "string"
                default: "4.896084471070842"
        responses:
            200:
                description: "Garbage collection details

                    Possible field values for the following attributes are defined as
                    follows

                    - aanbiedwijze

                    -- Aanbieden in minicontainer en vuilniszak

                    -- Wegbrengen naar afvalcontainer

                    -- Aanbieden in minicontainer of wegbrengen naar afvalpunt

                    -- Aanbieden in minicontainer

                    -- Aanbieden in minicontainer of wegbrengen naar afvalcontainer

                    -- Aanbieden in vuilniszak

                    -- Wegbrengen naar afvalpunt

                    - ophaaldag

                    free text, consists of comma seperated day names (e.g. 'vrijdag' or
                    'maandag,dinsdag') or free text (e.g. '2e woensdag van de maand' or
                    'Geen inzamelingsdagen')
                    "
                schema:
                    type: "object"
                    properties:
                        result:
                            type: "object"
                            properties:
                                features:
                                    type: "array"
                                    items:
                                        type: "object"
                                        properties:
                                            properties:
                                                type: "object"
                                                properties:
                                                    aanbiedwijze:
                                                        type: "string"
                                                    buurt_id:
                                                        type: "string"
                                                    dataset:
                                                        type: "string"
                                                    mutatatie:
                                                        type: "string"
                                                    naam:
                                                        type: "string"
                                                    ophaaldag:
                                                        type: "string"
                                                    opmerking:
                                                        type: "string"
                                                    stadsdeel_code:
                                                        type: "string"
                                                    stadsdeel_id:
                                                        type: "string"
                                                    stadsdeel_naam:
                                                        type: "string"
                                                    tijd_vanaf:
                                                        type: "string"
                                                        enum:
                                                            - "h:mm | hh:mm"
                                                    tijd_tot:
                                                        type: "string"
                                                        enum:
                                                            - "h:mm | hh:mm"
                                                    type:
                                                        type: "string"
                                                        enum:
                                                            - "Huisvuil | Huisafval | Grofvuil"
                                                    vollcode:
                                                        type: "string"
                                                    website:
                                                        type: "string"
                        type:
                            type: "string"
                            enum:
                                - "FeatureCollection"

            400:
              description: "missing x and y (rd) or Long / Lat parameters"

        """
        return self.dispatch_request()

    def dispatch_request(self):
        x, y = request.args.get('x'), request.args.get('y')

        if not x and request.args.get('lon'):
            x, y = request.args.get('lon'), request.args.get('lat'),
            in_4326 = Proj(init='epsg:4326')
            out_28992 = Proj(init='epsg:28992')
            x, y = transform(in_4326, out_28992, x, y)

        if x and y:
            point = WKTElement('POINT({} {})'.format(x, y), srid=28992)
            features = self.execute_query(point)
            return self.create_response(features)

        abort(400, 'missing x and y (rd) or Long / Lat parameters')

    def create_response(self, features):
        return jsonify({
            'result': {
                'type': 'FeatureCollection',
                'features': features
            }
        })

    def execute_query(self, point):
        features = []

        # huisvuil
        results = models.Huisvuil.query.filter(
            models.Huisvuil.geometrie.ST_Contains(point)).all()
        for row in results:
            features.append({
                'properties': {
                    'dataset': 'huisvuil',
                    'type': row.type,
                    'ophaaldag': row.ophaaldag,
                    'aanbiedwijze': row.aanbiedwijze,
                    'opmerking': row.opmerking,
                    'tijd_vanaf': row.tijd_vanaf,
                    'tijd_tot': row.tijd_tot,
                    'mutatie': row.mutatie,
                    'stadsdeel_id': row.stadsdeel_id,
                    'stadsdeel_naam': row.stadsdeel_naam,
                    'stadsdeel_code': row.stadsdeel_code,
                }
            })

        # grofvuil
        results = models.Grofvuil.query.filter(
            models.Grofvuil.geometrie.ST_Contains(point)).all()
        for row in results:
            features.append({
                'properties': {
                    'dataset': 'grofvuil',
                    'ophaaldag': row.ophaaldag,
                    'buurt_id': row.buurt_id,
                    'naam': row.naam,
                    'vollcode': row.vollcode,
                    'opmerking': row.opmerking,
                    'website': row.website,
                    'tijd_vanaf': row.tijd_vanaf,
                    'tijd_tot': row.tijd_tot,
                    'type': row.type,
                    'mutatie': row.mutatie,
                    'stadsdeel_id': row.stadsdeel_id,
                    'stadsdeel_naam': row.stadsdeel_naam,
                    'stadsdeel_code': row.stadsdeel_code,
                }
            })

        return features


class HealthDatabaseView(views.View):
    methods = ['GET']

    def get(self):
        return self.dispatch_request()

    def dispatch_request(self):
        try:
            connection = db.engine.connect()
            connection.close()
        except:
            return Response(
                'Database connectivity failed',
                content_type='text/plain', status=500)

        return Response('Connectivity OK', content_type='text/plain')


class HealthDataView(views.View):
    methods = ['GET']

    def get(self):
        return self.dispatch_request()

    def dispatch_request(self):
        try:
            assert models.Huisvuil.query.count() > 10
        except:
            return Response(
                'No huisvuil data', content_type='text/plain', status=500)

        try:
            assert models.Grofvuil.query.count() > 10
        except:
            return Response(
                'No grofvuil data', content_type='text/plain', status=500)

        return Response('Import data OK', content_type='text/plain')


application.add_url_rule('/search/', view_func=SearchView.as_view('search'))

application.add_url_rule(
    '/status/health/',
    view_func=HealthDatabaseView.as_view('health-database'))

application.add_url_rule(
    '/status/data/',
    view_func=HealthDataView.as_view('health-data'))


@application.route("/")
def usage():
    abort(400, 'missing x and y (rd) or Long / Lat parameters')


@application.route("/afvalophaalgebieden/spec.json")
def spec():
    try:
        swag = swagger(application)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "Afvalophaalgebieden API"
        return jsonify(swag)
    except Exception as error:
        return Response('Swagger generation failed: {}'.format(error), content_type='text/plain', status=500)


if __name__ == "__main__":
    from check_db import check_db
    check_db()

    application.run(host='0.0.0.0:8000')
