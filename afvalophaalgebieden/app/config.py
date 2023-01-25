import os


# Set in OpenStack config files.
OVERRIDE_HOST_ENV_VAR = 'DATABASE_HOST_OVERRIDE'
OVERRIDE_PORT_ENV_VAR = 'DATABASE_PORT_OVERRIDE'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

insecure_key = 'insecure'
DEBUG = False
TESTING = DEBUG

DB = {
    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'NAME': os.getenv('DB_NAME', 'afvalophaalgebieden'),
    'USER': os.getenv('DB_USER', 'afvalophaalgebieden'),
    'PASSWORD': os.getenv('DB_PASSWORD', 'insecure'),
    'HOST': os.getenv(OVERRIDE_HOST_ENV_VAR, 'database'),
    'PORT': os.getenv(OVERRIDE_PORT_ENV_VAR, '5432')
}

CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
    DB['USER'],
    DB['PASSWORD'],
    DB['HOST'],
    DB['PORT'],
    DB['NAME'],
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
POINT_DISTANCE_METERS = 50
