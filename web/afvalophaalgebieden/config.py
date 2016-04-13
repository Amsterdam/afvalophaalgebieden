import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    SECRET_KEY = os.getenv('SECRET_KEY', 'this-really-needs-to-be-changed')

    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@database/{}'.format(
        os.getenv('ATLAS_DB_NAME', 'postgres'),
        os.getenv('ATLAS_DB_PASSWORD', 'insecure'),
        os.getenv('ATLAS_DB_NAME', 'postgres')
    )
