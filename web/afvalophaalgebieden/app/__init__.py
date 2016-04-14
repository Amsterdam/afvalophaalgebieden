import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

testing = os.getenv('TESTING', False)

if testing:
    from . import config_test as config
else:
    from . import config_test

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
