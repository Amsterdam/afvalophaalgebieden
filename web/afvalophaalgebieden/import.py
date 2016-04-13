import argparse
import os

import shapefile
from shapely.geometry import Polygon
from shapely.wkb import loads, dumps

from app import models


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
        wkt = 'SRID=28992;%s' % loads(dumps(polygon)).wkt

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
            geometrie=wkt
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

if __name__ == '__main__':
    steps = list(jobs.keys())

    parser = argparse.ArgumentParser(description='Import afval ophaalgebieden')
    parser.add_argument('files', nargs='*',
                        help='run import (%s. defaults to all)' % ', '.join(steps))
    args = parser.parse_args()

    if not len(args.files):
        args.files = steps

    models.db.drop_all()
    models.db.create_all()

    for file in args.files:
        job = jobs[file]
        job.run()
