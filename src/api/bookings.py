"""
This file contains all API endpoints implementation connected with bookings.
"""
from flask_restplus import Resource


def register_bookings_endpoints(api):
    @api.route('/bookings')
    class Bookings(Resource):
        def get(self):
            """ Get all resources.

            Returns:
                sample response object
            """
            return {'sample': 'booking'}
