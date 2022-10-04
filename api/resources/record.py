import models
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
        parser.add_argument("username", type=str, help="Record username is required", required=True)
        parser.add_argument("encrypted_password", type=str, help="Encrypted password is required", required=True)
        args = parser.parse_args()

        record = models.Record(id=args["id"], name=args["name"], username=args["username"], 
                                encrypted_password=args["encrypted_password"], user_id=current_user.id)

        db.session.add(record)
        db.session.commit()

        return {"message": "Record created successfully"}, 201
    
    
    @token_required
    def delete(self):

        "Delete record"

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Record id is required", required=True)
        args = parser.parse_args()

        record = models.Record.query.filter_by(id=args["id"]).all()
        db.session.delete(record)
        db.session.commit()

        return 200



    