import os
import redis
from gcm import GCM

from config import gcm_api_key
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

mindme_api = Flask('mindme_api')

# API Configuration.
API_DEV_CONFIG = 'default-config.APIDevConfig'
API_CONFIG_FILE = os.environ.get('API_PRODUCTION_CONFIG', API_DEV_CONFIG)
mindme_api.config.from_object(API_CONFIG_FILE)

# DB configuration.
db = SQLAlchemy(mindme_api)

# Redis store
redis_store = redis.StrictRedis(host='localhost', port=6379, db=0)

# GCM client
gcm_client = GCM(gcm_api_key)

from app import views
from dbmodels import models
