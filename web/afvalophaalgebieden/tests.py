import unittest

from flask.ext.testing import TestCase

from app import models, config, factories, common
from run_import import ImportHuisvuil, ImportGrofvuil, ImportKleinChemisch


class TestImport(TestCase):
    def create_app(self):
        from app import app

        return app

    def setUp(self):
        models.db.drop_all()
        models.db.create_all()

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
        from app import app, db

        return app

    def setUp(self):
        models.db.drop_all()
        models.db.create_all()

        self.huisvuil = factories.HuisvuilFactory.create()
        self.grofvuil = factories.GrofvuilFactory.create()
        self.kleinchemisch = factories.KleinChemischFactory.create()

    def test_no_xy(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 500)

    def test_search(self):
        # import ipdb;ipdb.set_trace()
        response = self.client.get('/search/?x=%d&y=%d' % (20, 20))
        print(response.json)
        # print(response.json)

    def tearDown(self):
        models.db.session.remove()
        models.db.drop_all()


if __name__ == '__main__':
    unittest.main()
