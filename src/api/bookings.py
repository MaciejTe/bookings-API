"""
This file contains all API endpoints implementation connected with bookings.
"""
from datetime import datetime
from flask_restplus import Resource
from flask import jsonify, request

from src.database.models import db, Bookings
from src.api import api
from src.libs.helpers import validate_schema, error_response

ns = api.namespace("bookings", description="Bookings endpoint")

post_schema = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/root.json",
    "type": "object",
    "title": "The Root Schema",
    "required": ["resource_id", "user_id", "booked_from", "booked_to"],
    "properties": {
        "resource_id": {
            "$id": "#/properties/resource_id",
            "type": "integer",
            "title": "The Resource_id Schema",
            "default": 0,
            "examples": [4],
        },
        "user_id": {
            "$id": "#/properties/user_id",
            "type": "integer",
            "title": "The User_id Schema",
            "default": 0,
            "examples": [12],
        },
        "booked_from": {
            "$id": "#/properties/booked_from",
            "type": "string",
            "format": "date-time",
            "title": "The Booked_from Schema",
            "default": "",
            "examples": ["2019-04-10 10:00:00"],
            "pattern": "^(.*)$",
        },
        "booked_to": {
            "$id": "#/properties/booked_to",
            "type": "string",
            "format": "date-time",
            "title": "The Booked_to Schema",
            "default": "",
            "examples": ["2019-04-10 10:15:00"],
            "pattern": "^(.*)$",
        },
        "notes": {
            "$id": "#/properties/notes",
            "type": "string",
            "title": "The Notes Schema",
            "default": "",
            "examples": ["sample note"],
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
        "resource_id": {
            "$id": "#/properties/resource_id",
            "type": "integer",
            "title": "The Resource_id Schema",
            "default": 0,
            "examples": [4],
        },
        "booked_from": {
            "$id": "#/properties/booked_from",
            "type": "string",
            "title": "The Booked_from Schema",
            "default": "",
            "examples": ["2019-04-10 10:00:00"],
            "pattern": "^(.*)$",
        },
        "booked_to": {
            "$id": "#/properties/booked_to",
            "type": "string",
            "title": "The Booked_to Schema",
            "default": "",
            "examples": ["2019-04-10 10:15:00"],
            "pattern": "^(.*)$",
        },
        "notes": {
            "$id": "#/properties/notes",
            "type": "string",
            "title": "The Notes Schema",
            "default": "",
            "examples": ["sample note"],
            "pattern": "^(.*)$",
        },
    },
}


@ns.route("")
class BookingsEndpoint(Resource):
    """ Bookings endpoint. """

    def get(self):
        """ Get bookings data.

        Returns:
            bookings_list (list): list of bookings dictionaries
        """
        try:
            if request.get_json() is not None:
                return error_response(
                    "JSON body is not accepted in this endpoint",
                    msg="Invalid input",
                    err_code=406,
                )
            booking_id = request.args.get("id")
            resource_id = request.args.get("resource-id")
            user_id = request.args.get("user-id")
            if booking_id and user_id and resource_id is not None:
                bookings_obj_list = Bookings.query.filter_by(
                    id=booking_id, user_id=user_id, resource_id=resource_id
                ).all()
            elif booking_id is not None:
                bookings_obj_list = Bookings.query.filter_by(id=booking_id).all()
            elif user_id is not None:
                bookings_obj_list = Bookings.query.filter_by(user_id=user_id).all()
            elif resource_id is not None:
                bookings_obj_list = Bookings.query.filter_by(
                    resource_id=resource_id
                ).all()
            else:
                bookings_obj_list = Bookings.query.all()

            bookings_list = list()
            for booking in bookings_obj_list:
                booking_dict = {
                    "id": booking.id,
                    "resource_id": booking.resource_id,
                    "user_id": booking.user_id,
                    "booked_from": booking.booked_from,
                    "booked_to": booking.booked_to,
                    "notes": booking.notes,
                }
                bookings_list.append(booking_dict)
            return jsonify(bookings_list)
        except Exception as err:
            return error_response(err.__repr__())

    @validate_schema(post_schema)
    def post(self):
        """ Add single booking.

        Returns:
            response (flask.Response): Flask response object
        """
        request_data = request.get_json()
        try:
            db_data = Bookings(
                resource_id=request_data.get("resource_id"),
                user_id=request_data.get("user_id"),
                booked_from=datetime.strptime(
                    request_data.get("booked_from"), "%Y-%m-%d %H:%M:%S"
                ),
                booked_to=datetime.strptime(
                    request_data.get("booked_to"), "%Y-%m-%d %H:%M:%S"
                ),
                notes=request_data.get("notes"),
            )
            db.session.add(db_data)
            db.session.commit()
            return {
                "success": True,
                "message": f"Booking of user {request_data.get('resource_id')} "
                f"with resource {request_data.get('user_id')} "
                f"from {request_data.get('booked_from')} to "
                f"{request_data.get('booked_to')} added",
            }
        except Exception as err:
            return error_response(err.__repr__())

    @validate_schema(put_schema)
    def put(self):
        """ Update booking data.

        Returns:
            response (flask.Response): Flask response object
        """
        try:
            request_data = request.get_json()
            db_data = Bookings.query.filter_by(id=request_data.get("id")).first()
            if db_data is None:
                return error_response(
                    f"Booking with given ID: {request_data['id']} was not found",
                    msg="Booking not found",
                    err_code=404,
                )

            possible_request_params = [
                request_data.get("resource_id"),
                request_data.get("booked_from"),
                request_data.get("booked_to"),
            ]
            if not any(possible_request_params):
                return error_response(
                    f"'resource_id', 'booked_from' or 'booked_to' JSON arguments should be provided",
                    msg="Invalid input",
                    err_code=406,
                )
            if request_data.get("resource_id"):
                db_data.resource_id = request_data.get("resource_id")
            if request_data.get("booked_from"):
                db_data.booked_from = datetime.strptime(
                    request_data.get("booked_from"), "%Y-%m-%d %H:%M:%S"
                )
            if request_data.get("booked_to"):
                db_data.booked_to = datetime.strptime(
                    request_data.get("booked_to"), "%Y-%m-%d %H:%M:%S"
                )
            db.session.commit()
            return {"success": True, "message": f"Booking with ID {db_data.id} updated"}
        except (KeyError, AttributeError):
            return error_response(
                "ID is the only supported filter at this moment",
                msg="Unsupported filter",
                err_code=403,
            )
        except Exception as err:
            return error_response(err.__repr__())

    def delete(self):
        """ Delete given booking using its ID.

        Args:
            id (str): booking ID

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
            booking_id = request.args.get("id")
        else:
            return error_response(
                "Improper URL parameters provided", msg="Invalid input", err_code=406
            )
        try:
            db_data = Bookings.query.filter_by(id=booking_id).first()
            if db_data is None:
                return error_response(
                    f"Booking with given ID: {booking_id} was not found",
                    msg="Booking not found",
                    err_code=404,
                )
            db.session.delete(db_data)
            db.session.commit()
            response = jsonify(
                dict(success=True, message=f"Booking with ID {booking_id} removed")
            )
            return response
        except Exception as err:
            return error_response(err.__repr__())
