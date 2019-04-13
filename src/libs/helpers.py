from flask import jsonify, request
from jsonschema import Draft4Validator


def validate_schema(schema):
    """ Validate JSON schema decorator, applicable on all REST API methods.

    Args:
        schema (dict): expected JSON schema

    Returns:
        wrapper: JSON validator
    """
    validator = Draft4Validator(schema)

    def wrapper(fn):
        def validate_json(*args, **kwargs):
            """ Validate given JSON schema from HTTP request. """
            request_data = request.get_json(force=True)
            errors = [error.message for error in validator.iter_errors(request_data)]
            if errors:
                response = jsonify(
                    dict(success=False, message="Invalid input", errors=errors)
                )
                response.status_code = 406
                return response
            else:
                return fn(*args, **kwargs)

        return validate_json

    return wrapper


def error_response(err, msg="Internal server error", err_code=500):
    """

    Args:
        err (str): Raised exception string representation

    Returns:
        response (flask.Response): Flask response object
    """
    response = jsonify(dict(success=False, message=msg, errors=err))
    response.status_code = err_code
    return response
