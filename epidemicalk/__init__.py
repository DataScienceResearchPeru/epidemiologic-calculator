from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager

from .api.routes import api_bp
from .conf import Settings
from .database import bind_databases
from .management import database_cli
from .repositories import bind_repositories
from .services import bind_services
from .web import setup_web_routes

ROUTING_MODULES = [setup_web_routes]

MODULES_LIST = [
    bind_repositories,
    bind_services,
    bind_databases,
]


def register_extensions(application: Flask):
    application.register_blueprint(api_bp)
    jwt = JWTManager()
    jwt.init_app(application)


def create_app(application: Flask):
    register_extensions(application)
    application.config["SECRET_KEY"] = Settings.SECRET_KEY
    application.config["CORS_HEADERS"] = "Content-Type"
    application.config["TESTING"] = False
    application.config["MAIL_SERVER"] = Settings.MAIL_SERVER
    application.config["MAIL_PORT"] = Settings.MAIL_PORT
    application.config["MAIL_USE_TLS"] = Settings.MAIL_USE_TLS
    application.config["MAIL_USE_SSL"] = Settings.MAIL_USE_SSL
    application.config["MAIL_USERNAME"] = Settings.MAIL_USERNAME
    application.config["MAIL_PASSWORD"] = Settings.MAIL_PASSWORD
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    application.config.update(SQLALCHEMY_DATABASE_URI=Settings.DATABASE_URL)

    for routing in ROUTING_MODULES:
        routing(application)

    CORS(application)
    FlaskInjector(app=application, modules=MODULES_LIST)

    return application


app = Flask(__name__)
app.cli.add_command(database_cli)
app = create_app(app)
