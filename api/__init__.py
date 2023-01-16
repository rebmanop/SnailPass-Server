from flask import Flask
from flask_restful import Api
from config import Config, DevelopmentConfig, ProductionConfig


TOKEN_TTL = 10 #in minutes
NUMBER_OF_HASH_ITERATIONS = 40000

def create_app(config: Config):
    app = Flask(__name__)
    api = Api(app)

    app.config.from_object(config)
    
    from models import db
    db.init_app(app)

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


app = create_app(DevelopmentConfig())

