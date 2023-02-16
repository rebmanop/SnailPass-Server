import traceback
from typing import Tuple
from flask import jsonify, current_app
from sqlalchemy.orm.attributes import InstrumentedAttribute

MISSING_ARGUMENT_RESPONSE = "This JSON body argument is missing at all or it's value is null"
WRONG_FORMAT_ARGUMENT_RESPONSE = "This JSON body argument is in wrong format. Correct format is IV:Data"
EMPTY_STRING_ARGUMENT_RESPONSE = "This JSON body argument is an empty string"

def create_successful_response(message: str = "", status_code: int = 200) -> Tuple[dict, int]: 
    """Wraps successful response in a consistent format throughout the API"""
    return {"message": {"success" : message}}, status_code


def handle_exception(err):
        """Return custom JSON when APIError or its children are raised"""
        response = {}
        if len(err.args) > 0:
            response["message"] = {"error": f"{err.description}. {err.args[0]}"}
        current_app.logger.error(f"{err.description}: {err.args[0]}")
        return jsonify(response), err.code


def handle_unknown_exception(err):
    """Return JSON instead of HTML for any other server error"""
    current_app.logger.error(f"Unknown Exception: {str(err)}")
    current_app.logger.debug(''.join(traceback.format_exception(type(err), err, err.__traceback__)))
    response = {"error": "Unknown Error. Sorry, that error is on us, please contact support if this wasn't an accident"}
    return jsonify(response), 500


def handle_validation_exception(err):
    """
    Return custom JSON when APIDataFormatError is raised
    Used by custom data validator, so validation error response structure would look like request parser's error response structure
    """
    response = {}
    wrong_format_args =  err.args[0] 

    response["message"] = wrong_format_args
    return jsonify(response), err.code
        

def non_empty_string(s):
    """Custom type for request parser, checks for an empty string"""
    s = str(s)
    if not s:
        raise ValueError("Must not be empty string")
    return s






    