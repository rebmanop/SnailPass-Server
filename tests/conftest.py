import pytest
import os
from shutil import copy
from flask_restful import Api
from api import db
from models import *

from api import create_app


@pytest.fixture
def client():
    app = create_app()

    api = Api(app)
    app.config['SECRET_KEY'] = os.environ['SNAILPASS_SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///../tests/test_database.db"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
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

    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app.test_client()   # this is where the testing happens!
        db.drop_all()




