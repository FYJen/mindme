import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

mindme_api = Flask('mindme_api')

# API Configuration.
API_DEV_CONFIG = 'default-config.APIDevConfig'
API_CONFIG_FILE = os.environ.get('API_PRODUCTION_CONFIG', API_DEV_CONFIG)
mindme_api.config.from_object(API_CONFIG_FILE)

# DB configuration.
db = SQLAlchemy(mindme_api)