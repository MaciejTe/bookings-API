"""
This file contains SQLite database configuration.
"""
import os

from sqlalchemy.engine import Engine
from sqlalchemy import event

from src.database.models import db

cwd = os.path.dirname(os.path.abspath(__file__))
DATABASE_URI = 'sqlite:////{}/test.db'.format(cwd)
DB_ENGINE = db.create_engine('sqlite:////{}/test.db'.format(cwd))


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """ Listen for SQLAlchemy engine connection and set foreign keys support
        for SQLite.

    Args:
        dbapi_connection (object): database connection object
        connection_record (object):
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
