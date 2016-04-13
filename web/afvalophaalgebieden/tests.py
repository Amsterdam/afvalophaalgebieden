from flask.ext.testing import TestCase

from . import app
from . import models


class TestImport(TestCase):
    SQLALCHEMY_DATABASE_URI = 'postgres://database/main'
    TESTING = True

    def create_app(self):
        return app.app

    def setUp(self):
        models.db.create_all()

    def tearDown(self):
        models.db.session.remove()
        models.db.drop_all()
