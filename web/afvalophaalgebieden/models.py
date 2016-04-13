from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from sqlalchemy import Integer, String

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


class Huisvuil(db.Model):
    id = db.Column(Integer, primary_key=True)
    type = db.Column(String(254))
    ophaaldag = db.Column(String(254))
    aanbiedwij = db.Column(String(254))
    opmerking = db.Column(String(254))
    tijd_vanaf = db.Column(String(5))
    tijd_tot = db.Column(String(5))
    mutatie = db.Column(String(10))
    sdid = db.Column(Integer())
    sdnaam = db.Column(String(40))
    sdcode = db.Column(String(4))
    geometrie = db.Column(Geometry('MULTIPOLYGON'), srid=28992)

    def __repr__(self):
        return '<Huisvuil %r>' % self.type

    def __str__(self):
        return '<Huisvuil %r>' % self.type


class Grofvuil(db.Model):
    id = db.Column(Integer, primary_key=True)
    ophaaldag = db.Column(String(129))
    buurtid = db.Column(Integer())
    naam = db.Column(String(40))
    vollcode = db.Column(String(4))
    opmerking = db.Column(String(254))
    website = db.Column(String(254))
    tijd_vanaf = db.Column(String(254))
    tijd_tot = db.Column(String(5))
    type = db.Column(String(10))
    mutatie = db.Column(String(10))
    sdid = db.Column(Integer())
    sdnaam = db.Column(String(40))
    sdcode = db.Column(String(4))
    geometrie = db.Column(Geometry('MULTIPOLYGON'), srid=28992)

    def __repr__(self):
        return '<Grofvuil %r>' % self.type

    def __str__(self):
        return '<Grofvuil %r>' % self.type


class KCA(db.Model):
    id = db.Column(Integer, primary_key=True)
    type = db.Column(String(254))
    tijd_van = db.Column(String(254))
    tijd_tot = db.Column(String(254))
    dag = db.Column(String(254))
    mutatie = db.Column(String(10))
    sdid = db.Column(Integer())
    sdnaam = db.Column(String(40))
    sdcode = db.Column(String(4))
    geometrie = db.Column(Geometry('POINT'), srid=28992)

    def __repr__(self):
        return '<KCA %r>' % self.type

    def __str__(self):
        return '<KCA %r>' % self.type
