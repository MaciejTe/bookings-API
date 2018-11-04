"""
This file contains additional commands added to flask CLI.
"""
import os

from src import db

cwd = os.path.dirname(os.path.abspath(__file__))
DB_ENGINE = db.create_engine('sqlite:////{}/test.db'.format(cwd))


def register(app):
    """ Register additional command for Flask CLI.

    Args:
        app (flask app object): Flask application object
    """
    @app.cli.command('initdb')
    def init_db_command():
        """Initialize the database. """
        db.init_app(app)
        # need to trigger SQLite to turn on foreign key support
        connection = DB_ENGINE.connect()
        connection.close()
        db.create_all()
        app.logger.info('Database initialized')

    @app.cli.command('dropdb')
    def drop_db_command():
        """Drop the database. """
        db.init_app(app)
        db.drop_all()
        app.logger.info('Database dropped')
