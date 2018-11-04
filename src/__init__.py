"""
This file contains functional source of Booking API project.
"""
import logging

from flask import Flask
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from config import Config
from src.logger import handler

db = SQLAlchemy()


def create_app(config_class=Config):
    """ Prepare necessary parts of API system and create an application.

    Returns:
        app (flask app object): central object of Flask application
    """
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    db.init_app(app)
    # from src.api import bp as api_bp
    # app.register_blueprint(api_bp, url_prefix='/api')
    return app


def create_api(app):
    api = Api(app)
    return api
