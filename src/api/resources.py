"""
This file contains all API endpoints implementation connected with resources.
"""
from flask import jsonify
from flask_restplus import Resource

from src.database.models import Resources
from src.api import api

ns = api.namespace('resources', description='Resources endpoint')


@ns.route('')
class ResourcesEndpoint(Resource):
    def get(self):
        """ Get all resources.

        Returns:
            resources_list (list): list of resources dictionaries
        """
        resources_obj_list = Resources.query.all()
        resources_list = list()
        for res in resources_obj_list:
            res_dict = {
                'id': res.id,
                'title': res.title,
                'created_at': str(res.created_at),
                'updated_at': str(res.updated_at),
                'active': res.active
            }
            resources_list.append(res_dict)
        return jsonify(resources_list)

    def post(self, **kwargs):
        """ Add single resource.

        Returns:

        """
        res_data = Resources(**kwargs)
        print(res_data, 'PPP')
        return {'1': '2'}
