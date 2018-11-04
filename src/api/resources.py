"""
This file contains all API endpoints implementation connected with resources.
"""
from flask import jsonify

from src.api import bp
from src.database.models import db


@bp.route('/resources', methods=['GET'])
def get_resources():
    """ Get all resources.

    Returns:
        sample response object
    """
    return jsonify({'sample': 'resource'})
