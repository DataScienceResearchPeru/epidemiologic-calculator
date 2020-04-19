from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Binder, singleton

__all__ = ["bind_databases"]


def bind_databases(binder: Binder) -> Binder:
    application = binder.injector.get(Flask)
    db = SQLAlchemy(application)
    binder.bind(SQLAlchemy, to=db, scope=singleton)
    return binder
