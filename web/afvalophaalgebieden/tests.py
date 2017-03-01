import unittest

from flask_testing.utils import TestCase
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

        self.assertEqual(models.Huisvuil.query.count(), 147)

    def test_grofvuil_import(self):
        job = ImportGrofvuil()
        job.run()

        self.assertEqual(models.Grofvuil.query.count(), 460)

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

    # point in centrum amsterdam
    amsterdam_point = (120658, 486883)

    def create_app(self):
        from app import application

        return application

    def setUp(self):
        models.recreate_db()
        a = self.amsterdam_point
        # inside query
        test_poly = [(0, 0), (40, 0), (40, 40), (0, 40), (0, 0)]
        amsterdam_polygon = [(a[0] + p[0], a[1] + p[1]) for p in test_poly]
        polygon = Polygon(amsterdam_polygon)
        point = Point((a[0] + 25, a[1] + 25))

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
        test_poly = [(50, 50), (100, 0), (100, 100), (0, 100), (50, 50)]
        amsterdam_polygon = [(a[0] + p[0], a[1] + p[1]) for p in test_poly]
        polygon = Polygon(amsterdam_polygon)
        point = Point((a[0] + 100, a[1] + 100))

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
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        a = self.amsterdam_point
        response = self.client.get(
            '/search/?x=%d&y=%d' % (a[0] + 20, a[1] + 20))
        self.assertEqual(len(response.json['result']['features']), 3)

    def test_search_lon_lat(self):
        # a = rd + 20
        lat = 52.36894
        lon = 4.88326
        response = self.client.get(
            '/search/?lat={}&lon={}'.format(lat, lon))
        self.assertEqual(len(response.json['result']['features']), 3)

    def test_cors_header(self):
        a = self.amsterdam_point
        resp = self.client.get(
            '/search/?x=%d&y=%d' % (a[0] + 20, a[1] + 20),
            headers={'Origin': 'http://fee-fi-foo.fum'})
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual('*', resp.headers['Access-Control-Allow-Origin'])

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
