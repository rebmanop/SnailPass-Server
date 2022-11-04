import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

TOKEN_TTL = 30 #in minutes

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = os.environ['SNAILPASS_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SNAILPASS_DB_URI']


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

from api.resources.user import User
from api.resources.record import Record
from api.resources.additional_field import AdditionalField
from api.login import login_blueprint

api.add_resource(User, "/users")
api.add_resource(Record, "/records")
api.add_resource(AdditionalField, "/additional_fields")

app.register_blueprint(login_blueprint)