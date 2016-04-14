from flask import Flask, views
from flask_sqlalchemy import SQLAlchemy

from app import config

app = Flask(__name__)
app.config.update(config.SETTINGS)
db = SQLAlchemy(app)


class LocatieSearchView(views.View):
    methods = ['GET']

    def dispatch_request(self):
        pass


app.add_url_rule('/search/', view_func=LocatieSearchView.as_view('search'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
