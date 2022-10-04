import uuid
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

TOKEN_LIFETIME = 30 #in minutes

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)

from api.resources.user import User
from api.resources.record import Record
from api.login import login_blueprint

api.add_resource(User, "/users")
api.add_resource(Record, "/records")
app.register_blueprint(login_blueprint)










