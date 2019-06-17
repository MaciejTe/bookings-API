"""
This file is configured as FLASK_APP environment variable.
"""
import logging

from flask import Flask, Blueprint
from src.api.resources import ns as resources_namespace
from src.api.bookings import ns as bookings_namespace
from src.api.users import ns as users_namespace
from src.api.slots import ns as slots_namespace
from config import Config
from src.logger import handler
from src.api import api
from src.database import db
from src.cli import register_cli_commands


app = Flask(__name__, template_folder="templates")
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)


def initialize_app(flask_app):
    flask_app.config.from_object(Config)
    blueprint = Blueprint("swagger_ui", __name__, url_prefix="")

    api.init_app(blueprint)
    # api.add_namespace(resources_namespace)
    # api.add_namespace(bookings_namespace)
    # api.add_namespace(users_namespace)
    flask_app.register_blueprint(blueprint)
    register_cli_commands(flask_app)
    db.init_app(flask_app)


initialize_app(app)
# app.run()
