from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Binder, singleton
from sqlalchemy import MetaData

from repositories.sqlalchemy.mapping.user_mapping import user_mapping
from repositories.sqlalchemy.mapping.department_mapping import department_mapping
from repositories.sqlalchemy.mapping.province_mapping import province_mapping
from repositories.sqlalchemy.mapping.district_mapping import district_mapping
from utils import seed_data

app = Flask(__name__)


def configure_database_bindings(binder: Binder) -> Binder:
    application = binder.injector.get(Flask)
    metadata = MetaData()
    try:
        department_mapping(metadata)
        province_mapping(metadata)
        district_mapping(metadata)
        user_mapping(metadata)
        pass
    except Exception as e:
        print(e)

    db = SQLAlchemy(application)
    metadata.reflect(db.engine)
    metadata.drop_all(db.engine)
    db.session.commit()

    metadata.create_all(db.engine)
    db.session.commit()

    seed_data(db)

    binder.bind(SQLAlchemy, to=db, scope=singleton)
    return binder
