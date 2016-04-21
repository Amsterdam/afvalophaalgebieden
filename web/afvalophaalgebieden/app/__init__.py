from flask import Flask, request, views, jsonify, abort, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select, func, text
from geoalchemy2.elements import WKTElement

from . import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

from . import models

class SearchView(views.View):
    tables = ['grofvuil', 'huisvuil', 'klein_chemisch']

    methods = ['GET']

    def dispatch_request(self):
        x, y = request.args.get('x'), request.args.get('y')

        if x and y:
            point = WKTElement('POINT({} {})'.format(x, y), srid=28992)
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
            models.KleinChemisch.geometrie.ST_DWithin(point, app.config['POINT_DISTANCE_METERS'])
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
        except:
            return Response('Database connectivity failed', content_type='text/plain', status_code=500)

        return Response('Connectivity OK', content_type='text/plain')


class HealthDataView(views.View):
    methods = ['GET']

    def dispatch_request(self):
        try:
            assert models.Huisvuil.query.count() > 10
        except:
            return Response('No huisvuil data', content_type='text/plain', status_code=500)

        try:
            assert models.Grofvuil.query.count() > 10
        except:
            return Response('No grofvuil data', content_type='text/plain', status_code=500)

        try:
            assert models.KleinChemisch.query.count() > 10
        except:
            return Response('No KCA data', content_type='text/plain', status_code=500)

        return Response('Import data OK', content_type='text/plain')


app.add_url_rule('/search/', view_func=SearchView.as_view('search'))
app.add_url_rule('/status/health/', view_func=HealthDatabaseView.as_view('health-database'))
app.add_url_rule('/status/data/', view_func=HealthDataView.as_view('health-data'))
