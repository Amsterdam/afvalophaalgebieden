import os

from flask_sqlalchemy import SQLAlchemy
import shapefile
from shapely.geometry import Polygon
from geoalchemy2.shape import from_shape

from . import app, models

db = SQLAlchemy(app)


class ImportBase(object):
    path = 'shp'
    file = None
    fieldnames = list()

    def process_record(self, record):
        raise NotImplementedError

    def wrap_record(self, record):
        return dict(zip(self.fieldnames, record))

    def run(self):
        filename = self.resolve_file(self.file)
        sf = shapefile.Reader(filename)

        [self.fieldnames.append(properties[0]) for properties in sf.fields if isinstance(properties, list)]

        shape_recs = sf.shapeRecords()
        [self.process_record(rec) for rec in shape_recs]

    def resolve_file(self, code):
        matches = [os.path.join(self.path, f) for f in os.listdir(self.path) if code in f.lower()]
        if not matches:
            raise ValueError("Could not find file for %s in %s" % (code, self.path))
        matches_with_mtime = [(os.path.getmtime(f), f) for f in matches]
        match = sorted(matches_with_mtime)[-1]
        return match[1]


class ImportHuisvuil(ImportBase):
    file = 'huisvuil'
    types = {}

    def process_record(self, record):
        fields = self.wrap_record(record.record)

        polygon = Polygon([tuple(p) for p in record.shape.points])
        wkb_element = from_shape(polygon, srid=28992)

        model = models.Huisvuil(
            type=fields['type'].strip(),
            ophaaldag=fields['ophaaldag'].strip(),
            aanbiedwij=fields['aanbiedwij'].strip(),
            opmerking=fields['opmerking'].strip(),
            tijd_vanaf=fields['tijd_vanaf'].strip(),
            tijd_tot=fields['tijd_tot'].strip(),
            mutatie=fields['mutatie'].strip(),
            sdid=fields['sdid'],
            sdnaam=fields['sdnaam'].strip(),
            sdcode=fields['sdcode'].strip(),
            geometrie=wkb_element
        )
        models.db.session.add(model)
        models.db.session.commit()


class ImportGrofvuil(ImportBase):
    file = 'grofvuil'

    def process_record(self, record):
        pass
        model = models.Grofvuil(

        )


class ImportKleinChemisch(ImportBase):
    file = 'kcs'

    def process_record(self, record):
        pass
        model = models.KleinChemisch()


jobs = {
    'huisvuil': ImportHuisvuil(),
    'grofvuil': ImportGrofvuil(),
    'kca': ImportKleinChemisch()
}


def run():
    for file in jobs:
        job = jobs[file]
        job.run()
