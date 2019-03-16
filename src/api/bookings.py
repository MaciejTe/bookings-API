"""
This file contains all API endpoints implementation connected with bookings.
"""
from flask_restplus import Resource

from src.database.models import Bookings
from src.api import api

ns = api.namespace("bookings", description="Bookings endpoint")


@ns.route("")
class Bookings(Resource):
    """ Bookings endpoint. """

    def get(self):
        """ Get all bookings.

        Returns:
            sample response object
        """
        return {"sample": "booking"}
