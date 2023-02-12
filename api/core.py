from api.errors import APIError
from flask import jsonify
import traceback
import manage

@manage.app.errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    # Add some logging so that we can monitor different types of errors 
    manage.app.logger.error(f"{err.description}: {response['message']}")
    return jsonify(response), err.code

@manage.app.errorhandler(500)
def handle_unknown_exception(err):
    """Return JSON instead of HTML for any other server error"""
    manage.app.logger.error(f"Unknown Exception: {str(err)}")
    manage.app.logger.debug(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))
    response = {"error": "Sorry, that error is on us, please contact support if this wasn't an accident"}
    return jsonify(response), 500