"""
This file contains functional source of Booking API project.
"""
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from src.database.db_config import DATABASE_URI
import src.api


def create_app():
    """ Prepare necessary parts of API system and create an application.

    Returns:
        app (flask app object): central object of Flask application
    """
    handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    app = Flask(__name__, template_folder="templates")
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    from src.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    return app
