import unittest

from flask import Flask
from flask.ext.testing import TestCase
from flask_sqlalchemy import SQLAlchemy

from app import models, config
from import_job import ImportHuisvuil


class TestImport(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = config.SETTINGS['SQLALCHEMY_DATABASE_URI_TEST']
        db = SQLAlchemy(app)
        models.db = db

        return app

    def setUp(self):
        models.db.create_all()

    def test_import(self):
        job = ImportHuisvuil()
        job.run()
        import ipdb;ipdb.set_trace()

        self.assertEqual(models.Huisvuil.query.count(), 149)

    def tearDown(self):
        models.db.session.remove()
        models.db.drop_all()


if __name__ == '__main__':
    unittest.main()
