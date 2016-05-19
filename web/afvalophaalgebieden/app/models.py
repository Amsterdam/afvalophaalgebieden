from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from sqlalchemy import Integer, String

from app import application

db = SQLAlchemy(application)


def recreate_db():
    db.drop_all()
    with db.engine.connect() as c:
        c.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    db.create_all()


class Huisvuil(db.Model):
    id = db.Column(Integer, primary_key=True)
    type = db.Column(String(254), nullable=True)
    ophaaldag = db.Column(String(254), nullable=True)
    aanbiedwijze = db.Column(String(254), nullable=True)
    opmerking = db.Column(String(254), nullable=True)
    tijd_vanaf = db.Column(String(5), nullable=True)
    tijd_tot = db.Column(String(5), nullable=True)
    mutatie = db.Column(String(10), nullable=True)
    stadsdeel_id = db.Column(String(20), nullable=True)
    stadsdeel_naam = db.Column(String(40), nullable=True)
    stadsdeel_code = db.Column(String(4), nullable=True)
    geometrie = db.Column(Geometry('POLYGON', srid=28992), nullable=True)

    def __repr__(self):
        return '<Huisvuil %r>' % self.type

    def __str__(self):
        return '<Huisvuil %r>' % self.type


class Grofvuil(db.Model):
    id = db.Column(Integer, primary_key=True)
    ophaaldag = db.Column(String(129), nullable=True)
    buurt_id = db.Column(String(129), nullable=True)
    naam = db.Column(String(40), nullable=True)
    vollcode = db.Column(String(4), nullable=True)
    opmerking = db.Column(String(254), nullable=True)
    website = db.Column(String(254), nullable=True)
    tijd_van = db.Column(String(254), nullable=True)
    tijd_tot = db.Column(String(5), nullable=True)
    type = db.Column(String(10), nullable=True)
    mutatie = db.Column(String(10), nullable=True)
    stadsdeel_id = db.Column(String(20), nullable=True)
    stadsdeel_naam = db.Column(String(40), nullable=True)
    stadsdeel_code = db.Column(String(4), nullable=True)
    geometrie = db.Column(Geometry('POLYGON', srid=28992), nullable=True)

    def __repr__(self):
        return '<Grofvuil %r>' % self.naam

    def __str__(self):
        return '<Grofvuil %r>' % self.naam


class KleinChemisch(db.Model):
    id = db.Column(Integer, primary_key=True)
    type = db.Column(String(254), nullable=True)
    tijd_van = db.Column(String(254), nullable=True)
    tijd_tot = db.Column(String(254), nullable=True)
    dag = db.Column(String(254), nullable=True)
    mutatie = db.Column(String(10), nullable=True)
    stadsdeel_id = db.Column(String(20), nullable=True)
    stadsdeel_naam = db.Column(String(40), nullable=True)
    stadsdeel_code = db.Column(String(4), nullable=True)
    geometrie = db.Column(Geometry('POINT', srid=28992), nullable=True)

    def __repr__(self):
        return '<Kleinchemischafval %r>' % self.type

    def __str__(self):
        return '<Kleinchemischafval %r>' % self.type
