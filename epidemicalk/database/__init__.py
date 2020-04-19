from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Binder, singleton
from sqlalchemy import MetaData

from epidemicalk.repositories.mapping.department import department
from epidemicalk.repositories.mapping.district import district
from epidemicalk.repositories.mapping.province import province
from epidemicalk.repositories.mapping.user import user

__all__ = ["bind_databases"]


def bind_databases(binder: Binder) -> Binder:
    application = binder.injector.get(Flask)
    db = SQLAlchemy(application)
    metadata = MetaData()

    department(metadata)
    province(metadata)
    district(metadata)
    user(metadata)

    binder.bind(SQLAlchemy, to=db, scope=singleton)
    return binder
