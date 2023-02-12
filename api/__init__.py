from flask import Flask
from flask_restful import Api
import os
from config import config, Config
from flask_migrate import Migrate
from api.errors import APIError
from flask import jsonify
import traceback
from api.core import *


TOKEN_TTL = 10.0 #in minutes
NUMBER_OF_HASH_ITERATIONS = 40000
IV_AND_DATA_DELIMETER  = ':'

def create_app(test_config: Config = None):
    app = Flask("snailpass-rest-api")

    
    # @app.errorhandler(APIError)
    # def handle_exception(err):
    #     """Return custom JSON when APIError or its children are raised"""
    #     response = {"error": err.description, "message": ""}
    #     if len(err.args) > 0:
    #         response["message"] = err.args[0]
    #     # Add some logging so that we can monitor different types of errors 
    #     app.logger.error(f"{err.description}: {response['message']}")
    #     return jsonify(response), err.code

    # @app.errorhandler(500)
    # def handle_unknown_exception(err):
    #     """Return JSON instead of HTML for any other server error"""
    #     app.logger.error(f"Unknown Exception: {str(err)}")
    #     app.logger.debug(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))
    #     response = {"error": "Sorry, that error is on us, please contact support if this wasn't an accident"}
    #     return jsonify(response), 500
    
    api = Api(app)

    if test_config:
        app.config.from_object(test_config)
    else:
        env = os.environ.get("SNAILPASS_CONFIGURATION")
        app.config.from_object(config[env])

    
    from models import db
    db.init_app(app)
    Migrate(app, db)


    from api.resources.user import User
    from api.resources.record import Record
    from api.resources.additional_field import AdditionalField
    from api.resources.note import Note
    from api.login import login_blueprint

    api.add_resource(User, "/users")
    api.add_resource(Record, "/records")
    api.add_resource(AdditionalField, "/additional_fields")
    api.add_resource(Note, "/notes")

    app.register_blueprint(login_blueprint)
    return app




