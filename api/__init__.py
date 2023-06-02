import os
from flask import Flask
from flask_restful import Api
from api.config import config, Config
from api.errors import APIError, APIDataFormatError
from celery import Celery


TOKEN_TTL = 10.0  # in minutes
EMAIL_CONFIRMATION_TTL = 60.0
NUMBER_OF_HASH_ITERATIONS = 40000
DATA_AND_IV_DELIMETER = ":"

celery = Celery(__name__, broker="redis://redis:6379/0")


def create_app(test_config: Config = None) -> Flask:
    app = Flask("SnailPass-Server-API")
    api = Api(app)

    celery.conf.update(app.config)

    if test_config:
        app.config.from_object(test_config)
    else:
        env = os.environ.get("SNAILPASS_CONFIGURATION")
        app.config.from_object(config[env])

    from api.models import db

    db.init_app(app)

    from api.mail import mail

    mail.init_app(app)

    from api.resources.user import User
    from api.resources.record import Record
    from api.resources.additional_field import AdditionalField
    from api.resources.note import Note
    from api.login import login_blueprint
    from api.email_confirmation import email_confirmation_blueprint
    from api.favicon import favicon_blueprint
    from api.index import index_blueprint

    api.add_resource(User, "/users")
    api.add_resource(Record, "/records")
    api.add_resource(AdditionalField, "/additional_fields")
    api.add_resource(Note, "/notes")

    from api.core import (
        handle_exception,
        handle_unknown_exception,
        handle_validation_exception,
    )

    app.register_error_handler(APIError, handle_exception)
    app.register_error_handler(500, handle_unknown_exception)
    app.register_error_handler(Exception, handle_unknown_exception)
    app.register_error_handler(APIDataFormatError, handle_validation_exception)

    app.register_blueprint(login_blueprint)
    app.register_blueprint(email_confirmation_blueprint)
    app.register_blueprint(favicon_blueprint)
    app.register_blueprint(index_blueprint)
    return app
