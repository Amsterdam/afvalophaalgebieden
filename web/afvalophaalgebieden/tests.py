import unittest

from flask.ext.testing import TestCase
from geoalchemy2.shape import from_shape
from shapely.geometry import Polygon, Point

from app import models, factories
from run_import import ImportHuisvuil, ImportGrofvuil, ImportKleinChemisch


class TestImport(TestCase):
    def create_app(self):
        from app import application

        return application

    def setUp(self):
        models.recreate_db()

    def test_huisvuil_import(self):
        job = ImportHuisvuil()
        job.run()

        self.assertEqual(models.Huisvuil.query.count(), 149)

    def test_grofvuil_import(self):
        job = ImportGrofvuil()
        job.run()

        self.assertEqual(models.Grofvuil.query.count(), 496)

    def test_kca_import(self):
        job = ImportKleinChemisch()
        job.run()

        self.assertEqual(models.KleinChemisch.query.count(), 81)

    def tearDown(self):
        models.db.session.remove()
        models.db.drop_all()


class TestApi(TestCase):
    huisvuil = None
    grofvuil = None
    kleinchemisch = None

    def create_app(self):
        from app import application

        return application

    def setUp(self):
        models.recreate_db()

        # inside query
        polygon = Polygon([(0, 0), (40, 0), (40, 40), (0, 40), (0, 0)])
        point = Point((25, 25))

        factories.HuisvuilFactory.create(
            geometrie=from_shape(polygon, srid=28992)
        )
        factories.GrofvuilFactory.create(
            geometrie=from_shape(polygon, srid=28992)
        )
        factories.KleinChemischFactory.create(
            geometrie=from_shape(point, srid=28992)
        )

        # outside query
        polygon = Polygon([(50, 50), (100, 0), (100, 100), (0, 100), (50, 50)])
        point = Point((100, 100))

        factories.HuisvuilFactory.create(
            geometrie=from_shape(polygon, srid=28992)
        )
        factories.GrofvuilFactory.create(
            geometrie=from_shape(polygon, srid=28992)
        )
        factories.KleinChemischFactory.create(
            geometrie=from_shape(point, srid=28992)
        )

    def test_no_xy(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 400)

    def test_search(self):
        response = self.client.get('/search/?x=%d&y=%d' % (20, 20))
        self.assertEqual(len(response.json['result']['features']), 3)

    def test_cors_header(self):
        resp = self.client.get('/search/?x=%d&y=%d' % (20, 20), headers={'Origin': 'http://fee-fi-foo.fum'})
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEquals('*', resp.headers['Access-Control-Allow-Origin'])

    def tearDown(self):
        models.db.session.remove()
        models.db.drop_all()


class TestHealth(TestCase):
    def create_app(self):
        from app import application

        return application

    def setUp(self):
        pass

    def test_database(self):
        response = self.client.get('/status/health/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
