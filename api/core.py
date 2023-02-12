import traceback
from flask import jsonify, current_app

ARGUMENT_MISSING_RESPONSE = " is missing at all, value is null or value is empty"


def handle_exception(err):
        """Return custom JSON when APIError or its children are raised"""
        response = {}
        if len(err.args) > 0:
            response["error"] = f"{err.description}. {err.args[0]}"
        # Add some logging so that we can monitor different types of errors 
        current_app.logger.error(f"{err.description}: {err.args[0]}")
        return jsonify(response), err.code


def handle_unknown_exception(err):
    """Return JSON instead of HTML for any other server error"""
    current_app.logger.error(f"Unknown Exception: {str(err)}")
    current_app.logger.debug(''.join(traceback.format_exception(type(err), err, err.__traceback__)))
    response = {"error": "Unknown Error. Sorry, that error is on us, please contact support if this wasn't an accident"}
    return jsonify(response), 500


def non_empty_string(s):
    """Custom type for request parser, checks for an empty string"""
    s = str(s)
    if not s:
        raise ValueError("Must not be empty string")
    return s




    