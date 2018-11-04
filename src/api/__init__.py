# from flask import Blueprint

# bp = Blueprint('api', __name__)
#
# from src.api import bookings, resources
from src.api.resources import register_resources_endpoints
from src.api.bookings import register_bookings_endpoints


def register_endpoints(api):
    resources.register_resources_endpoints(api)
    bookings.register_bookings_endpoints(api)
