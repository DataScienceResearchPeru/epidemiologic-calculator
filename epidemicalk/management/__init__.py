from flask import current_app
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from epidemicalk.database.utils import seed_data
from epidemicalk.repositories.mapping.department import department
from epidemicalk.repositories.mapping.district import district
from epidemicalk.repositories.mapping.province import province
from epidemicalk.repositories.mapping.user import user

database_cli = AppGroup("database")


@database_cli.command("migrate")
def migrate():
    db = SQLAlchemy(current_app)

    metadata = MetaData()

    department(metadata)
    province(metadata)
    district(metadata)
    user(metadata)

    metadata.reflect(db.engine)
    metadata.create_all(db.engine)

    db.session.commit()


@database_cli.command("drop")
def drop():
    db = SQLAlchemy(current_app)

    metadata = MetaData()
    metadata.drop_all(db.engine)

    db.session.commit()


@database_cli.command("load_fixtures")
def load_fixtures():
    db = SQLAlchemy(current_app)

    metadata = MetaData()

    department(metadata)
    province(metadata)
    district(metadata)
    user(metadata)

    seed_data(db)

    db.session.commit()
