"""
This file contains all API endpoints implementation connected with resources.
"""
from flask import jsonify
from flask_restplus import Resource

# from src.api import bp
from src.database.models import Resources
from src import db


def register_resources_endpoints(api):
    @api.route('/resources')
    class ResourcesEndpoint(Resource):
        def get(self):
            """ Get all resources.

            Returns:
                sample response object
            """
            print(Resources.query.all(), '<<<')
            return {'sample': 'resource'}

# @api.route('/resources2', methods=['GET'])
# def get_resources():
#     """ Get all resources.
#
#     Returns:
#         sample response object
#     """
#     return jsonify({'sample': 'resource'})
