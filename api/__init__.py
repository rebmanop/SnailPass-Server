from flask import Flask
from flask_restful import Api
import os
from config import config, Config
from flask_migrate import Migrate
TOKEN_TTL = 10.0 #in minutes
NUMBER_OF_HASH_ITERATIONS = 40000

def create_app(test_config: Config = None):
    app = Flask("snailpass-rest-api")
    api = Api(app)

    if test_config:
        app.config.from_object(test_config)
    else:
        env = os.environ.get("FLASK_DEBUG")
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




