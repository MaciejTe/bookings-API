"""
This file contains additional commands added to flask CLI.
"""
from src.database.db_config import DB_ENGINE
from src.database.models import db


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
