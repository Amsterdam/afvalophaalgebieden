import os
import re


def get_docker_host():
    """
    Looks for the DOCKER_HOST environment variable to find the VM
    running docker-machine.

    If the environment variable is not found, it is assumed that
    you're running docker on localhost.
    """
    d_host = os.getenv('DOCKER_HOST', None)
    if d_host:
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', d_host):
            return d_host

        return re.match(r'tcp://(.*?):\d+', d_host).group(1)
    return 'localhost'


def in_docker():
    """
    Checks pid 1 cgroup settings to check with reasonable certainty we're in a
    docker env.
    :return: true when running in a docker container, false otherwise
    """
    try:
        return ':/docker/' in open('/proc/1/cgroup', 'r').read()
    except:
        return False


OVERRIDE_HOST_ENV_VAR = 'DATABASE_HOST_OVERRIDE'
OVERRIDE_PORT_ENV_VAR = 'DATABASE_PORT_OVERRIDE'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LocationKey:
    local = 'local'
    docker = 'docker'
    override = 'override'


def get_database_key():
    if os.getenv(OVERRIDE_HOST_ENV_VAR):
        return LocationKey.override
    elif in_docker():
        return LocationKey.docker

    return LocationKey.local


DATABASE_OPTIONS = {
    LocationKey.docker: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'afvalophaalgebieden'),
        'USER': os.getenv('DB_USER', 'afvalophaalgebieden'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'insecure'),
        'HOST': 'database',
        'PORT': '5432'
    },
    LocationKey.local: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'afvalophaalgebieden'),
        'USER': os.getenv('DB_USER', 'afvalophaalgebieden'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'insecure'),
        'HOST': get_docker_host(),
        'PORT': '5405'
    },
    LocationKey.override: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'afvalophaalgebieden'),
        'USER': os.getenv('DB_USER', 'afvalophaalgebieden'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'insecure'),
        'HOST': os.getenv(OVERRIDE_HOST_ENV_VAR),
        'PORT': os.getenv(OVERRIDE_PORT_ENV_VAR, '5432')
    },
}

insecure_key = 'insecure'
SECRET_KEY = os.getenv('SECRET_KEY', insecure_key)
DEBUG = SECRET_KEY == insecure_key
TESTING = DEBUG

DB = DATABASE_OPTIONS[get_database_key()]

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
