"""
This file contains all API endpoints implementation connected with slots.
"""
from flask import jsonify, request
from flask_restplus import Resource
from sqlalchemy import and_, func

from src.api import api
from src.database.models import Slots
from src.libs.helpers import error_response

ns = api.namespace("slots", description="Slots endpoint")


@ns.route("")
class SlotsEndpoint(Resource):
    """ Slots endpoint. """

    def get(self):
        """ Get slots endpoint.

        Returns:
            slots_list (list): list of slots dictionaries
        """
        try:
            if request.get_json() is not None:
                return error_response(
                    "JSON body is not accepted in this endpoint",
                    msg="Invalid input",
                    err_code=406,
                )
            from_date = request.args.get("from")
            to_date = request.args.get("to")
            resources = request.args.get("resources")
            if from_date and to_date and resources is not None:
                slots_obj_list = Slots.query.filter_by(
                    timestamp=from_date,
                    timestamp_end=to_date,
                    available_resources=resources).all()
            elif from_date and to_date is not None:
                slots_obj_list = Slots.query.filter(
                    and_(
                        func.date(Slots.timestamp) >= from_date),
                        func.date(Slots.timestamp) <= to_date).all()
            elif from_date is not None:
                slots_obj_list = Slots.query.filter(
                    func.date(Slots.timestamp) == from_date).all()
            elif to_date is not None:
                slots_obj_list = Slots.query.filter(
                    func.date(Slots.timestamp_end) == to_date).all()
            elif resources is not None:
                slots_obj_list = Slots.query.filter(Slots.available_resources.in_(resources)).all()
            else:
                slots_obj_list = Slots.query.all()

            slots_list = list()
            for slot in slots_obj_list:
                slot_dict = {
                    "id": slot.id,
                    "timestamp": str(slot.timestamp),
                    "timestamp_end": str(slot.timestamp_end),
                    "formatted_timestamp": str(slot.formatted_timestamp),
                    "formatted_timestamp_end": str(slot.formatted_timestamp_end),
                    "free": slot.free,
                    "available_resources": slot.available_resources,
                    "maximum_capacity": slot.maximum_capacity
                }
                slots_list.append(slot_dict)
            return jsonify(slots_list)
        except Exception as err:
            return error_response(err.__repr__())
