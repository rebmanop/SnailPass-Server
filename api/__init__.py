from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from api.resources.user import User
from api.resources.record import Record

api.add_resource(User, "/users")
api.add_resource(Record, "/records")

