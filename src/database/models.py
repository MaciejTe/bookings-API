"""
This file contains database models declared with SQLAlchemy ORM.
"""
from datetime import datetime

from src.database import db


class Bookings(db.Model):
    """ Create bookings database table. """

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey("resources.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    booked_from = db.Column(db.DateTime, nullable=False)
    booked_to = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String)

    def __repr__(self):
        # TODO: change notes to something meaningful
        return "<Booking: {}>" % self.notes


class Slots(db.Model):
    """ Create slots database table. """

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    timestamp_end = db.Column(db.DateTime, nullable=False)
    formatted_timestamp = db.Column(db.String, nullable=False)
    formatted_timestamp_end = db.Column(db.String, nullable=False)
    free = db.Column(db.Boolean, nullable=False)
    available_resources = db.Column(db.String, nullable=False)
    maximum_capacity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Slot - Start: {} End: {} Free: {}>".format(
            self.formatted_timestamp, self.formatted_timestamp_end, self.free
        )


class Resources(db.Model):
    """ Create resources database table. """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    intervals = db.Column(db.String, nullable=False)
    opening_hours_mon = db.Column(db.String)
    opening_hours_tue = db.Column(db.String)
    opening_hours_wed = db.Column(db.String)
    opening_hours_thu = db.Column(db.String)
    opening_hours_fri = db.Column(db.String)
    opening_hours_sat = db.Column(db.String)
    opening_hours_sun = db.Column(db.String)

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
        return "<User: {} {} {}>".format(self.name, self.email, self.phonenumber)
