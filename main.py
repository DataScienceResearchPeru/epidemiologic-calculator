import jinja2
from flask import Flask
from flask_injector import FlaskInjector
from flask_sqlalchemy import SQLAlchemy
from injector import Binder, singleton
from sqlalchemy import MetaData

from environment_config import EnvironmentConfig
from repositories.configuration import configure_repositories_binding
from repositories.sqlalchemy.mapping.user_mapping import user_mapping
from web.configuration import configure_web_route
from api.routes import api_bp

templates_folders = [
    EnvironmentConfig.TEMPLATE_DIR,
]

ROUTING_MODULES = [
    configure_web_route
]


def configure_database_bindings(binder: Binder) -> Binder:
    application = binder.injector.get(Flask)
    metadata = MetaData()
    try:
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

    binder.bind(SQLAlchemy, to=db, scope=singleton)
    return binder


modules_list = [
    configure_repositories_binding,
    configure_database_bindings
]


def create_app(templates_folders_list=templates_folders, modules=modules_list):
    application = Flask(__name__)

    application.register_blueprint(api_bp)
    application.config['SECRET_KEY'] = EnvironmentConfig.SECRET_KEY
    application.config['TESTING'] = True
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config.update(
        SQLALCHEMY_DATABASE_URI=EnvironmentConfig.DATABASE
    )

    for routing in ROUTING_MODULES:
        routing(application)

    custom_loader = jinja2.ChoiceLoader([
        application.jinja_loader,
        jinja2.FileSystemLoader(templates_folders_list)
    ])

    FlaskInjector(app=application, modules=modules)
    application.jinja_loader = custom_loader

    return application


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=EnvironmentConfig.PORT, debug=EnvironmentConfig.MODE_DEBUGGER)