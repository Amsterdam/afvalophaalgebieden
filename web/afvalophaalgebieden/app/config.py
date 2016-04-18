import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = False
TESTING = False
CSRF_ENABLED = True
SECRET_KEY = os.getenv('SECRET_KEY', 'this-really-needs-to-be-changed')
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
    os.getenv('DB_NAME', 'postgres'),
    os.getenv('DB_PASSWORD', 'insecure'),
    os.getenv('DOCKER_HOST', 'localhost'),
    os.getenv('DOCKER_PORT', 5405),
    os.getenv('DB_NAME', 'postgres'),
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
