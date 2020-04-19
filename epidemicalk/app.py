from flask import Flask

from . import create_app
from .management import database_cli

app = Flask(__name__)
app.cli.add_command(database_cli)
EPICAL_APP = create_app(app)
