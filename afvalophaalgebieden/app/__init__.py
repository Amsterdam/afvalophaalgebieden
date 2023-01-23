import logging

from flask import Flask, request, views, jsonify, abort, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
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
                    'ophalen': row.ophalen,
                    'frequentie': row.frequentie,
                    'ophaaldag': row.ophaaldag,
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


@application.route("/openapi.yaml")
def yaml_spec():
    with open('./app/afvalophaalgebieden.swagger.yaml', 'r') as yaml:
        yaml = yaml.read()
    return Response(yaml, content_type='text/plain')


if __name__ == "__main__":
    from check_db import check_db
    check_db()

    application.run(host='0.0.0.0:8000')
