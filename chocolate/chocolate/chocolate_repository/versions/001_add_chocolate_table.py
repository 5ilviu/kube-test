from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.postgresql import UUID

meta = MetaData()

chocolate_entity = Table(
    'chocolate', meta,
    Column('id', UUID, primary_key=True),
    Column('name', String(100)),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    chocolate_entity.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    chocolate_entity.drop()
