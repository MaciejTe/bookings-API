"""
This file contains all API endpoints implementation connected with resources.
"""
from datetime import datetime
from flask import jsonify, request
from flask_restplus import Resource

from src.api import api
from src.database.models import db, Users
from src.libs.helpers import validate_schema, error_response

ns = api.namespace("users", description="Users endpoint")


post_schema = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/root.json",
    "type": "object",
    "title": "The Root Schema",
    "required": ["name", "email", "phonenumber"],
    "properties": {
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The Name Schema",
            "default": "",
            "examples": ["Test User"],
            "pattern": "^(.*)$",
        },
        "email": {
            "$id": "#/properties/email",
            "type": "string",
            "title": "The Email Schema",
            "default": "",
            "examples": ["testmail@gmail.com"],
            "pattern": "^(.*)$",
        },
        "phonenumber": {
            "$id": "#/properties/phonenumber",
            "type": "string",
            "title": "The Phonenumber Schema",
            "default": "",
            "examples": ["666666666"],
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
    "required": ["id"],
    "properties": {
        "id": {
            "$id": "#/properties/id",
            "type": "integer",
            "title": "The Id Schema",
            "default": 0,
            "examples": [4],
        },
        "phonenumber": {
            "$id": "#/properties/phonenumber",
            "type": "string",
            "title": "The Phonenumber Schema",
            "default": "",
            "examples": ["124124"],
            "pattern": "^(.*)$",
        },
        "email": {
            "$id": "#/properties/email",
            "type": "string",
            "title": "The Email Schema",
            "default": "",
            "examples": ["jacek@gmail.com"],
            "pattern": "^(.*)$",
        },
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The Name Schema",
            "default": "",
            "examples": ["Andrew Golota"],
            "pattern": "^(.*)$",
        },
    },
}


@ns.route("")
class UsersEndpoint(Resource):
    """ Users endpoint. """

    def get(self):
        """ Get users endpoint.

        Returns:
            users_list (list): list of users dictionaries
        """
        try:
            if request.get_json() is not None:
                return error_response(
                    "JSON body is not accepted in this endpoint",
                    msg="Invalid input",
                    err_code=406,
                )
            user_id = request.args.get("id")
            name = request.args.get("name")
            if user_id and name is not None:
                users_obj_list = Users.query.filter_by(id=user_id, name=name).all()
            elif user_id is not None:
                users_obj_list = Users.query.filter_by(id=user_id).all()
            elif name is not None:
                users_obj_list = Users.query.filter_by(name=name).all()
            else:
                users_obj_list = Users.query.all()

            users_list = list()
            for user in users_obj_list:
                user_dict = {
                    "id": user.id,
                    "name": user.name,
                    "created_at": str(user.created_at),
                    "updated_at": str(user.updated_at),
                    "email": user.email,
                    "phonenumber": user.phonenumber,
                }
                users_list.append(user_dict)
            return jsonify(users_list)
        except Exception as err:
            return error_response(err.__repr__())

    @validate_schema(post_schema)
    def post(self):
        """ Add single user.

        Returns:
            response (flask.Response): Flask response object
        """
        request_data = request.get_json()
        try:
            db_data = Users(
                name=request_data.get("name"),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                email=request_data.get("email"),
                phonenumber=request_data.get("phonenumber"),
            )
            db.session.add(db_data)
            db.session.commit()
            return {
                "success": True,
                "message": f"User {request_data.get('name')} added",
            }
        except Exception as err:
            return error_response(err.__repr__())

    @validate_schema(put_schema)
    def put(self):
        """ Update user data.

        Returns:
            response (flask.Response): Flask response object
        """
        try:
            request_data = request.get_json()
            db_data = Users.query.filter_by(id=request_data.get("id")).first()
            if db_data is None:
                return error_response(
                    f"User with given ID: {request_data['id']} was not found",
                    msg="User not found",
                    err_code=404,
                )
            possible_request_params = [
                request_data.get("name"),
                request_data.get("email"),
                request_data.get("phonenumber"),
            ]
            if not any(possible_request_params):
                return error_response(
                    f"'name', 'email' or 'phonenumber' JSON arguments should be provided",
                    msg="Invalid input",
                    err_code=406,
                )
            if request_data.get("name"):
                db_data.name = request_data.get("name")
            if request_data.get("email"):
                db_data.email = request_data.get("email")
            if request_data.get("phonenumber"):
                db_data.phonenumber = request_data.get("phonenumber")
            db.session.commit()
            return {"success": True, "message": f"User with ID {db_data.id} updated"}
        except (KeyError, AttributeError):
            return error_response(
                "ID is the only supported filter at this moment",
                msg="Unsupported filter",
                err_code=403,
            )
        except Exception as err:
            return error_response(err.__repr__())

    def delete(self):
        """ Delete given user using his ID.

        Args:
            id (str): user ID

        Returns:
            response (flask.Response): Flask response object
        """
        if request.get_json() is not None:
            return error_response(
                "JSON body is not accepted in this endpoint",
                msg="Invalid input",
                err_code=406,
            )
        if request.args.get("id"):
            user_id = request.args.get("id")
        else:
            return error_response(
                "Improper URL parameters provided", msg="Invalid input", err_code=406
            )
        try:
            db_data = Users.query.filter_by(id=user_id).first()
            if db_data is None:
                return error_response(
                    f"User with given ID: {user_id} was not found",
                    msg="User not found",
                    err_code=404,
                )
            db.session.delete(db_data)
            db.session.commit()
            response = jsonify(
                dict(success=True, message=f"User with ID {user_id} removed")
            )
            return response
        except Exception as err:
            return error_response(err.__repr__())
