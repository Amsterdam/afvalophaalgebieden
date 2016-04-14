from .config import *
import os

DEBUG = True
TESTING = True
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/test'.format(
    os.getenv('ATLAS_DB_NAME', 'postgres'),
    os.getenv('ATLAS_DB_PASSWORD', 'insecure'),
    os.getenv('DOCKER_HOST', 'localhost'),
    os.getenv('DOCKER_PORT', 5405),
)
