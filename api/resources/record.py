import database
from api import db
from flask_restful import Resource, reqparse

class Record(Resource):
    
    def post():
        """Create new record"""

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Record id is required", required=True)
        parser.add_argument("name", type=str, help="Name of the record is required", required=True)
        parser.add_argument("username", type=str, help="Record username is required", required=True)
        parser.add_argument("encrypted_password", type=str, help="Encrypted password is required", required=True)
        parser.add_argument("user_id", type=str, help="User id is required", required=True)
        args = parser.parse_args()

        record = database.Record(id=args["id"], name=args["name"], uesername=args["username"], 
                                encrypted_password=["encrypted_password"], user_id=["user_id"])

        db.session.add(record)
        db.session.commit()

        return record, 200


    def delete():
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Record id is required", required=True)
        args = parser.parse_args()

        record = database.User.query.filter_by(id=args["id"]).all()
        db.session.delete(record)
        db.session.commit()

        return 200



    