import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = False
TESTING = False
CSRF_ENABLED = True
SECRET_KEY = os.getenv('SECRET_KEY', 'this-really-needs-to-be-changed')
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
    os.getenv('DB_NAME', 'postgres'),
    os.getenv('DB_PASSWORD', 'insecure'),
    os.getenv('DB_HOST', 'localhost'),
    os.getenv('DB_PORT_5432', 5405),
    os.getenv('DB_NAME', 'postgres'),
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
POINT_DISTANCE_METERS = 50
