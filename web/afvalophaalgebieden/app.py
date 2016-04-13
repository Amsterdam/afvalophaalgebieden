from flask import Flask, request, views, jsonify, abort
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
from sqlalchemy.sql import select, func

app = Flask(__name__)
app.config.from_object('config')


class LocatieSearchView(views.View):
    methods = ['GET']

    def dispatch_request(self):
        pass


app.add_url_rule('/search/', view_func=LocatieSearchView.as_view('search'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
