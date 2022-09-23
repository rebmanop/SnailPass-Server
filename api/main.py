from flask_restful import Resource, reqparse
from api import db, app, api


sign_up_args = reqparse.RequestParser()
sign_up_args.add_argument("login", type=str, help = "Login is required", required=True)
sign_up_args.add_argument("master_password_hash", type=str, help = "Hash of the master password is required", required=True)


class UserModel(db.Model):
    id = db.Column(db.String, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    master_password_hash = db.Column(db.String(100), nullable=False)
    hint = db.Column(db.Column(db.String(100)), nullable=True)

    def __repr__(self):
      return f"id: {self.id}, login: {self.login}"


class PasswordModel(db.Model):
    id = db.Column(db.String, primary_key=True)
    encrypted_password = db.column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"id: {self.id}, encrypted_password: {self.encrypted_password}, user_id: {self.user_id}"


db.create_all()

class SignUp(Resource):
    def post(self):
        pass


class LogIn(Resource): 
    def get(self):
        pass
    



api.add_resource(SignUp, "/signup")


if __name__ == "__main__":
    app.run(debug=True)

