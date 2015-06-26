import os

baseDir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseDir, 'mindme.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(baseDir, 'db_repository')
