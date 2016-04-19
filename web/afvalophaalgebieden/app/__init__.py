from flask import Flask, request, views, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select, func, text
from geoalchemy2.elements import WKTElement

from . import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

from . import models

class SearchView(views.View):
    default_columns = ['id', 'display', 'type', 'uri']
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
                    'type': row.type
                }
            })

        # grofvuil
        results = models.Grofvuil.query.filter(models.Grofvuil.geometrie.ST_Contains(point)).all()
        for row in results:
            features.append({
                'properties': {
                    'naam': row.naam
                }
            })

        # kleinchemisch
        results = models.KleinChemisch.query.filter(models.KleinChemisch.geometrie.ST_DWithin(point, 10)).all()
        for row in results:
            features.append({
                'properties': {
                    'type': row.type
                }
            })

        return features


app.add_url_rule('/search/', view_func=SearchView.as_view('search'))
