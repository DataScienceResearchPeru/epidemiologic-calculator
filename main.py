import jinja2
from environment_config import EnvironmentConfig
from flask import Flask
from web.configuration import configure_web_route
from api.routes import api_bp

from flask_cors import CORS, cross_origin

templates_folders = [
    EnvironmentConfig.TEMPLATE_DIR,
]

ROUTING_MODULES = [
    configure_web_route
]


def create_app(templates_folders_list=templates_folders):
    application = Flask(__name__)

    application.register_blueprint(api_bp)
    application.config['SECRET_KEY'] = EnvironmentConfig.SECRET_KEY
    application.config['TESTING'] = True
    
    cors = CORS(application)
    application.config['CORS_HEADERS'] = 'Content-Type'

    for routing in ROUTING_MODULES:
        routing(application)

    custom_loader = jinja2.ChoiceLoader([
        application.jinja_loader,
        jinja2.FileSystemLoader(templates_folders_list)
    ])

    application.jinja_loader = custom_loader

    return application


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=EnvironmentConfig.PORT, debug=EnvironmentConfig.MODE_DEBUGGER)