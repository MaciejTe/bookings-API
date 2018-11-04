"""
This file contains SQLite database configuration.
"""
from sqlalchemy.engine import Engine
from sqlalchemy import event


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
