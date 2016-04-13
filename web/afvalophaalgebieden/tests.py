from app import app
from flask.ext.testing import TestCase


class SearchTest(TestCase):
    SQLALCHEMY_DATABASE_URI = 'postgres://database/main'

    def create_app(self):
        return app

    def setUp(self):
        pass
