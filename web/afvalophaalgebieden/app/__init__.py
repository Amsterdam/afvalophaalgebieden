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
            return self.create_response(self.execute_query(point))

        abort(500)

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
        results = models.KleinChemisch.query.filter(models.KleinChemisch.geometrie.ST_DWithin(point, 10)).all()
        for row in results:
            features.append({
                'properties': {
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


class HealthView(views.View):
    methods = ['GET']

    def dispatch_request(self):
        # TODO add something usefull here
        return Response('Connectivity OK', content_type='text/plain')


app.add_url_rule('/search/', view_func=SearchView.as_view('search'))
app.add_url_rule('/status/health/', view_func=HealthView.as_view('health'))
