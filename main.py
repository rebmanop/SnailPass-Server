from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    master_password_hash = db.Column(db.String(100), nullable=False)
    hint = db.Column(db.Column(db.String(100)), nullable=True)


class PasswordsModel(db.Model):
    pass

db.create_all()

sign_up_args = reqparse.RequestParser()
sign_up_args.add_argument("login", type=str, help = "Login is required", required=True)
sign_up_args.add_argument("master_password_hash", type=str, help = "Hash of the master password is required", required=True)


class SignUp(Resource):
    def put(self):
        pass


api.add_resource(SignUp, "/signup")

if __name__ == "__main__":
    app.run(debug=True)

