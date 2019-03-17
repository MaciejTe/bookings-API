"""
This file contains all API endpoints implementation connected with resources.
"""
from datetime import datetime
from flask import jsonify, request
from flask_restplus import Resource

from src.api import api
from src.database.models import db, Resources
from src.libs.helpers import validate_schema, error_response

ns = api.namespace("resources", description="Resources endpoint")


post_schema = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/root.json",
    "type": "object",
    "title": "The Root Schema",
    "required": ["active", "title"],
    "properties": {
        "active": {
            "$id": "#/properties/active",
            "type": "boolean",
            "title": "The Active Schema",
            "default": False,
            "examples": [True],
        },
        "title": {
            "$id": "#/properties/title",
            "type": "string",
            "title": "The Title Schema",
            "default": "",
            "examples": ["Sample 3"],
            "pattern": "^(.*)$",
        },
    },
}

put_schema = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/root.json",
    "type": "object",
    "title": "The Root Schema",
    "required": ["active"],
    "properties": {
        "active": {
            "$id": "#/properties/active",
            "type": "boolean",
            "title": "The Active Schema",
            "default": False,
            "examples": [False],
        }
    },
}


@ns.route("")
class ResourcesEndpoint(Resource):
    """ Resources endpoint. """
    def get(self):
        """ Get all resources.

        Returns:
            resources_list (list): list of resources dictionaries
        """
        try:
            if request.get_json() is not None:
                return error_response(
                    "JSON body is not accepted in this endpoint",
                    msg="Invalid input",
                    err_code=406,
                )
            resource_id = request.args.get("id")
            title = request.args.get("title")
            if resource_id and title is not None:
                resources_obj_list = Resources.query.filter_by(
                    id=resource_id, title=title).all()
            elif resource_id is not None:
                resources_obj_list = Resources.query.filter_by(id=resource_id).all()
            elif title is not None:
                resources_obj_list = Resources.query.filter_by(title=title).all()
            else:
                resources_obj_list = Resources.query.all()
            resources_list = list()
            for res in resources_obj_list:
                res_dict = {
                    "id": res.id,
                    "title": res.title,
                    "created_at": str(res.created_at),
                    "updated_at": str(res.updated_at),
                    "active": res.active,
                }
                resources_list.append(res_dict)
            return jsonify(resources_list)
        except Exception as err:
            return error_response(err.__repr__())

    @validate_schema(post_schema)
    def post(self):
        """ Add single resource.

        Returns:
            response (flask.Response): Flask response object
        """
        request_data = request.get_json()
        try:
            db_data = Resources(
                title=request_data.get("title"),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                active=request_data.get("active"),
            )
            db.session.add(db_data)
            db.session.commit()
            return {
                "success": True,
                "message": f"Resource {request_data.get('title')} added",
            }
        except Exception as err:
            return error_response(err.__repr__())

    @validate_schema(put_schema)
    def put(self):
        """ Update resource data.

        Returns:
            response (flask.Response): Flask response object
        """
        try:
            request_data = request.get_json()
            db_data = Resources.query.filter_by(id=request_data.get("id")).first()
            if db_data is None:
                return error_response(
                    f"Resource with given ID: {request_data['id']} was not found",
                    msg="Resource not found",
                    err_code=404,
                )
            db_data.active = request_data.get("active")
            db.session.commit()
            return {
                "success": True,
                "message": f"Resource with ID {db_data.id} updated",
            }
        except (KeyError, AttributeError):
            return error_response(
                "ID is the only supported filter at this moment",
                msg="Unsupported filter",
                err_code=403
            )
        except Exception as err:
            return error_response(err.__repr__())

    def delete(self):
        """ Delete given resource using its ID.

        Args:
            id (str): resource ID

        Returns:
            response (flask.Response): Flask response object
        """
        if request.get_json() is not None:
            return error_response(
                "JSON body is not accepted in this endpoint",
                msg="Invalid input",
                err_code=406,
            )
        if request.args.get("id") is not None:
            resource_id = request.args.get("id")
        else:
            return error_response(
                "Improper URL parameters provided", msg="Invalid input", err_code=406
            )
        try:
            db_data = Resources.query.filter_by(id=resource_id).first()
            if db_data is None:
                return error_response(
                    f"Resource with given ID: {resource_id} was not found",
                    msg="Resource not found",
                    err_code=404,
                )
            db.session.delete(db_data)
            db.session.commit()
            response = jsonify(
                dict(success=True, message=f"Resource with ID {resource_id} removed")
            )
            return response
        except Exception as err:
            return error_response(err.__repr__())
