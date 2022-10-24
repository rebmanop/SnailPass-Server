import models
import datetime
from api import db
from flask_restful import Resource, reqparse
from api.access_restrictions import token_required

class Record(Resource):
    @token_required
    def post(self, current_user):
        
        """Create new record"""

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Record id is required", required=True)
        parser.add_argument("name", type=str, help="Name of the record is required", required=True)
        parser.add_argument("login", type=str, help="Record login is required", required=True)
        parser.add_argument("encrypted_password", type=str, help="Encrypted password is required", required=True)
        args = parser.parse_args()

        record = models.Record(id=args["id"], name=args["name"], login=args["login"], 
                                encrypted_password=args["encrypted_password"], user_id=current_user.id, creation_time=datetime.datetime.now())

        db.session.add(record)
        db.session.commit()

        return {"message": f"Record '{args['name']}' created successfully (user = '{current_user.email}')"}, 201
    
    
    @token_required
    def delete(self, current_user):

        "Delete record"

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Record id is required", required=True)
        args = parser.parse_args()

        record = models.Record.query.filter_by(id=args["id"]).all()
        db.session.delete(record)
        db.session.commit()

        return {"message": f"Record '{args['name']}' deleted successfully (user = '{current_user.email}')"}, 200



    