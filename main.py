import jinja2

from flask import Flask
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from environment_config import EnvironmentConfig
from repositories.configuration import configure_repositories_binding
from services.configuration import configure_services_binding
from configuration_database import configure_database_bindings, app
from web.configuration import configure_web_route
from api.routes import api_bp


templates_folders = [
    EnvironmentConfig.TEMPLATE_DIR,
]

ROUTING_MODULES = [
    configure_web_route
]

modules_list = [
    configure_repositories_binding,
    configure_services_binding,
    configure_database_bindings
]


def register_extensions(application: Flask):
    application.register_blueprint(api_bp)
    jwt = JWTManager()
    jwt.init_app(application)


def create_app(application, templates_folders_list=templates_folders, modules=modules_list):
    register_extensions(application)

    application.config['SECRET_KEY'] = EnvironmentConfig.SECRET_KEY
    cors = CORS(application)
    application.config['CORS_HEADERS'] = 'Content-Type'

    application.config['TESTING'] = False
    application.config['MAIL_SERVER'] = EnvironmentConfig.MAIL_SERVER
    application.config['MAIL_PORT'] = EnvironmentConfig.MAIL_PORT
    application.config['MAIL_USE_TLS'] = EnvironmentConfig.MAIL_USE_TLS
    application.config['MAIL_USE_SSL'] = EnvironmentConfig.MAIL_USE_SSL
    application.config['MAIL_USERNAME'] = EnvironmentConfig.MAIL_USERNAME
    application.config['MAIL_PASSWORD'] = EnvironmentConfig.MAIL_PASSWORD

    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config.update(
        SQLALCHEMY_DATABASE_URI=EnvironmentConfig.DATABASE_URL
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


app = create_app(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=EnvironmentConfig.PORT, debug=EnvironmentConfig.MODE_DEBUGGER)