# utf-8

import os
import argparse
import shapefile
from geoalchemy2.shape import from_shape
from shapely.geometry import Polygon

from app import models


class ImportBase(object):
    # path = 'shp'
    file = None
    fieldnames = list()

    def __init__(self, path):
        self.fieldnames = list()
        self.path = path

    def process_record(self, record):
        raise NotImplementedError

    def creatNullFromByteSpaces(self, rec):
        if isinstance(rec, bytes):
            field_raw = rec.strip()
            return None
        elif isinstance(rec, str):
            return rec.strip()
        else:
            return rec

    def wrap_record(self, record):
        record = [self.creatNullFromByteSpaces(rec) for rec in record]
        #print(record)
        return dict(zip(self.fieldnames, record))

    def run(self):
        print('processing: %s' % self.file)
        filename = self.resolve_file(self.file)
        sf = shapefile.Reader(filename)

        [self.fieldnames.append(properties[0]) for properties in sf.fields if isinstance(properties, list)]

        shape_recs = sf.shapeRecords()
        [self.process_record(rec) for rec in shape_recs]

    def resolve_file(self, code):
        """
        Resolves to most recent path containing code.
        :param code: filename code, e.g.: "huisvuil"
        :return: path to .shp file
        """
        matches = [os.path.join(self.path, f) for f in os.listdir(self.path) if code in f.lower() and '.shp' in f]
        if not matches:
            raise ValueError("Could not find file for %s in %s" % (code, self.path))
        matches_with_mtime = [(os.path.getmtime(f), f) for f in matches]
        match = sorted(matches_with_mtime)[-1]
        return match[1]


class ImportHuisvuil(ImportBase):
    file = 'huisvuil'

    def process_record(self, record):
        fields = self.wrap_record(record.record)

        if record.shape.points == []:
            return
        else:
            polygon = Polygon(record.shape.points)
            # print(r'{}'.format(polygon))

        wkb_element = from_shape(polygon, srid=28992)

        model = models.Huisvuil(
            type=fields['type'],
            ophaaldag=fields['ophaaldag'],
            aanbiedwijze=fields['aanbiedwij'],
            opmerking=fields['opmerking'],
            tijd_vanaf=fields['tijd_vanaf'],
            tijd_tot=fields['tijd_tot'],
            mutatie=fields['mutatie'],
            stadsdeel_id=fields['sdid'],
            stadsdeel_naam=fields['sdnaam'],
            stadsdeel_code=fields['sdcode'],
            geometrie=wkb_element
        )
        models.db.session.add(model)
        models.db.session.commit()


class ImportGrofvuil(ImportBase):
    file = 'grofvuil'

    def process_record(self, record):
        fields = self.wrap_record(record.record)

        if record.shape.points == []:
            return
        else:
            polygon = Polygon([tuple(p) for p in record.shape.points])

        wkb_element = from_shape(polygon, srid=28992)

        model = models.Grofvuil(
            ophalen=fields['ophalen'],
            frequentie=fields['frequentie'],
            ophaaldag=fields['ophaaldag'],
            opmerking=fields['opmerking'],
            buurt_id=fields['buurtid'],
            naam=fields['naam'],
            vollcode=fields['vollcode'],
            website=fields['website'],
            tijd_vanaf=fields['tijd_vanaf'],
            tijd_tot=fields['tijd_tot'],
            type=fields['type'],
            mutatie=fields['mutatie'],
            stadsdeel_id=fields['sdid'],
            stadsdeel_naam=fields['sdnaam'],
            stadsdeel_code=fields['sdcode'],
            geometrie=wkb_element
        )
        models.db.session.add(model)
        models.db.session.commit()


def parser():
    parser = argparse.ArgumentParser(description='Run import shapefile to postgres database')
    parser.add_argument('path', help='Insert folder location where the unzipped shapefiles are, for example: /data')
    return parser


def run_all():
    args = parser().parse_args()

    huisvuil_import = ImportHuisvuil(args.path)
    huisvuil_import.run()

    grofvuil_import = ImportGrofvuil(args.path)
    grofvuil_import.run()


if __name__ == '__main__':
    models.db.drop_all()
    models.db.create_all()

    run_all()
