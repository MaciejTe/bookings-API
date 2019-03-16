"""
This file contains database models declared with SQLAlchemy ORM.
"""
from datetime import datetime

from src.database import db


class Bookings(db.Model):
    """ Create bookings database table. """

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey("resources.id"), nullable=False)
    service_id = db.Column(db.Integer, nullable=False)
    booked_from = db.Column(db.DateTime, nullable=False, default=datetime.now)
    booked_to = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String)

    def __repr__(self):
        # TODO: change notes to something meaningful
        return "<Booking: {}>" % self.notes


class Resources(db.Model):
    """ Create resources database table. """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "<Resource: {}>".format(self.title)


class Users(db.Model):
    """ Create users database table. """

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phonenumber = db.Column(db.String)

    def __repr__(self):
        return "<User: {}>".format(self.title)
