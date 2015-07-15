from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
message = Table('message', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('message', TEXT, nullable=False),
    Column('created_date', DATETIME),
    Column('last_time_modified_date', DATETIME),
    Column('status_id', INTEGER, nullable=False),
)

message = Table('message', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('message', Text, nullable=False),
    Column('created_date', DateTime),
    Column('last_modified_date', DateTime),
    Column('status_id', Integer, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['message'].columns['last_time_modified_date'].drop()
    post_meta.tables['message'].columns['last_modified_date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['message'].columns['last_time_modified_date'].create()
    post_meta.tables['message'].columns['last_modified_date'].drop()
