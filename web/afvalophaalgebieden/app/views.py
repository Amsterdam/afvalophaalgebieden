from flask import Flask, request, views, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
from sqlalchemy.sql import select, func

from .models import Huisvuil, Grofvuil, KleinChemisch


class GeoSearchView(views.View):
    default_columns = ['id', 'display', 'type', 'uri']
    tables = ['grofvuil', 'huisvuil', 'klein_chemisch']

    methods = ['GET']

    def dispatch_request(self):
        x, y = request.args.get('x'), request.args.get('y')

        if x and y:
            point = 'POINT({} {})'.format(x, y)

        if point:
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
        features = list()

        query = session.query(Huisvuil).filter(Huisvuil.geometrie.ST_Contains(point))
        for row in query:
            features.append({
                'properties': row
            })
        using = 'USING rsid=28992 USING UNIQUE id'

        for table in self.tables:
            for view in layer_config['views']:
                geo_column, properties = self.inspect_view(view, connection)
                columns = self.default_columns
                where = select.where(func.ST_Contains(geo_column, point))

                if wgs84:
                    geo_column += '_wgs84'

                if 'openbareruimte' in view:
                    columns.append('opr_type')

                if layer_config['operator'] == 'dwithin':
                    where = func.ST_DWithin(geo_column, point)

                s = select(columns, where.where(using), view)
                result = connection.execute(s)

                if result:
                    for row in result:
                        features.append({
                            'properties': row
                        })

        return features

    def get_connection(self, bind):
        if bind not in self.connections:
            engine = create_engine(app.config.DATABASE_BINDS[bind])
            self.connections[bind] = engine.connect()

        return self.connections[bind]

    def inspect_view(self, view, connection):
        # return tuple of geometrie field and non-geometry fields from the given view
        geo_field, properties = None, list()

        cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM {} LIMIT 0'.format(view))

        fields = [desc[0] for desc in cur.description]

        for f in fields:
            if 'geo' in f:
                geo_field = f
            else:
                properties.append(f)

        return geo_field, properties

app.add_url_rule('/geosearch/', view_func=GeoSearchView.as_view('geosearch'))
