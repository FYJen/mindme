from db import db_config

class BasicConfig(object):
    SQLALCHEMY_DATABASE_URI = db_config.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_MIGRATE_REPO = db_config.SQLALCHEMY_MIGRATE_REPO

class APIDevConfig(BasicConfig):
    DEBUG = True

# TODO: Enable production in a bit.
#
# class APIProductionConfig(BasicConfig):
#     DEBUG = False
#     SERVER_NAME = 'www.arthur-jen.com'
