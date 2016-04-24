import logging

from flask import Flask, request, views, jsonify, abort, Response
from flask.ext.cors import CORS
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2.elements import WKTElement

from . import config

application = Flask(__name__)
log_handler = logging.StreamHandler()

logging.basicConfig(level=logging.INFO)

application.config.from_object(config)
application.logger.addHandler(log_handler)

CORS(application, resources={r'/search/*': {'origins': config.CORS_ORIGINS}}, methods=['GET', 'OPTIONS'])

db = SQLAlchemy(application)

from . import models        # vreemde locatie, maar moet ná het definieren van application


class SearchView(views.View):
    tables = ['grofvuil', 'huisvuil', 'klein_chemisch']

    methods = ['GET']

    def dispatch_request(self):
        x, y, rd = request.args.get('x'), request.args.get('y'), request.args.get('rd', True)
        srid = 28992 if rd else 32651

        if x and y:
            point = WKTElement('POINT({} {})'.format(x, y), srid=srid)
            features = self.execute_query(point)
            return self.create_response(features)

        abort(400)

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
        results = models.Huisvuil.query.filter(models.Huisvuil.geometrie.ST_Contains(point)).all()
        for row in results:
            features.append({
                'properties': {
                    'dataset': 'huisvuil',
                    'type': row.type,
                    'ophaaldag': row.ophaaldag,
                    'aanbiedwijk': row.aanbiedwijk,
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
        results = models.Grofvuil.query.filter(models.Grofvuil.geometrie.ST_Contains(point)).all()
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
                    'tijd_van': row.tijd_van,
                    'tijd_tot': row.tijd_tot,
                    'type': row.type,
                    'mutatie': row.mutatie,
                    'stadsdeel_id': row.stadsdeel_id,
                    'stadsdeel_naam': row.stadsdeel_naam,
                    'stadsdeel_code': row.stadsdeel_code,
                }
            })

        # kleinchemisch
        results = models.KleinChemisch.query.filter(
            models.KleinChemisch.geometrie.ST_DWithin(point, application.config['POINT_DISTANCE_METERS'])
        ).all()
        for row in results:
            features.append({
                'properties': {
                    'dataset': 'kca',
                    'type': row.type,
                    'tijd_van': row.tijd_van,
                    'tijd_tot': row.tijd_tot,
                    'dag': row.dag,
                    'mutatie': row.mutatie,
                    'stadsdeel_id': row.stadsdeel_id,
                    'stadsdeel_naam': row.stadsdeel_naam,
                    'stadsdeel_code': row.stadsdeel_code,
                }
            })

        return features


class HealthDatabaseView(views.View):
    methods = ['GET']

    def dispatch_request(self):
        try:
            connection = db.engine.connect()
            connection.close()
        except:
            return Response('Database connectivity failed', content_type='text/plain', status=500)

        return Response('Connectivity OK', content_type='text/plain')


class HealthDataView(views.View):
    methods = ['GET']

    def dispatch_request(self):
        try:
            assert models.Huisvuil.query.count() > 10
        except:
            return Response('No huisvuil data', content_type='text/plain', status=500)

        try:
            assert models.Grofvuil.query.count() > 10
        except:
            return Response('No grofvuil data', content_type='text/plain', status=500)

        try:
            assert models.KleinChemisch.query.count() > 10
        except:
            return Response('No KCA data', content_type='text/plain', status=500)

        return Response('Import data OK', content_type='text/plain')


application.add_url_rule('/search/', view_func=SearchView.as_view('search'))
application.add_url_rule('/status/health/', view_func=HealthDatabaseView.as_view('health-database'))
application.add_url_rule('/status/data/', view_func=HealthDataView.as_view('health-data'))


if __name__ == "__main__":
    from check_db import check_db
    check_db()

    application.run(host='0.0.0.0:8000')
