import models
import datetime
from models import db
from api.access_restrictions import token_required
from flask_restful import Resource, marshal, reqparse
from flask_restful import Resource, reqparse, request
from api.resource_fields import RECORD_RESOURCE_FIELDS


class Record(Resource):
    @token_required
    def post(self, current_user):
        
        """Create new record"""

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Record id is missing", required=True)
        parser.add_argument("name", type=str, help="Record name is missing", required=True)
        parser.add_argument("login", type=str, help="Record login is missing", required=True)
        parser.add_argument("encrypted_password", type=str, help="Encrypted password is missing", required=True)
        parser.add_argument("nonce", type=str, help="Nonce is missing", required=True)
        args = parser.parse_args()

        if models.Record.query.get(args["id"]):
            return {"message": f"Record with id '{args['id']}' already exist"}, 409
        
        records_with_requested_name = models.Record.query.filter_by(user_id=current_user.id, name=args["name"]).all()
        
        for record_with_requested_name in records_with_requested_name:
            if record_with_requested_name.login == args["login"]:
                return {"message": f"Record with name '{args['name']}' and with login '{args['login']}' already exist in current user's vault"}, 409
                
        record = models.Record(id=args["id"], name=args["name"], login=args["login"], 
                                encrypted_password=args["encrypted_password"], user_id=current_user.id, creation_time=datetime.datetime.now(), 
                                update_time=datetime.datetime.now(), nonce=args["nonce"])

                                
        db.session.add(record)
        db.session.commit()
        return {"message": f"Record '{args['name']}' created successfully (user = '{current_user.email}')"}, 201


    
    @token_required
    def patch(self, current_user):
        
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Record id is missing", required=True)
        parser.add_argument("name", type=str, help="Record name is missing", required=True)
        parser.add_argument("login", type=str, help="Record login is missing", required=True)
        parser.add_argument("encrypted_password", type=str, help="Record encrypted password is missing", required=True)
        parser.add_argument("is_favorite", type=bool, help="Record 'is_favorite' status is missing", required=True)
        parser.add_argument("is_deleted", type=bool, help="Record 'is_deleted' status is missing", required=True)
        parser.add_argument("nonce",  type=str, help="Record nonce is missing", required=True)
        args = parser.parse_args()

        record = models.Record.query.get(args["id"])

        if not record:
            return {"message": f"Record with id '{args['id']}' doesn't exist"}, 404
        
        if current_user.id != record.user_id:
            return {"message": f"Record with id '{record.id}' doesn't belong to the current user"}, 403
        
        record_with_same_login_and_name = db.session.query(models.Record).filter(models.Record.id != record.id,
                            models.Record.name == args["name"], models.Record.login == args["login"]).first()

        if record_with_same_login_and_name:
            return {"message": f"Record with name '{args['name']}' and with login '{args['login']}' already exist in current user's vault"}, 409
        

        record.name = args["name"]
        record.login = args["login"]
        record.encrypted_password = args["encrypted_password"]
        record.nonce = args["nonce"]
        record.is_favorite = args["is_favorite"]
        record.is_deleted = args["is_deleted"]
        record.update_time = datetime.datetime.now()
        
        db.session.commit()
        return {"message": f"Changes for the record '{args['id']}' were successfully made"}, 200

    

    @token_required
    def delete(self, current_user):

        "Delete record"

        record_id = request.args.get("id")

        if not record_id:
            return {"message": f"Record id is missing in uri args"}, 400

        record = models.Record.query.get(record_id)

        if not record:
            return {"message": "Record with that id doesn't exist"}, 404

        if current_user.id != record.user_id:
            return {"message": f"Record with id '{record.id}' doesn't belong to the current user"}, 403

        
        db.session.delete(record)
        db.session.commit()

        return {"message": f"Record '{record.name}' deleted successfully (user = '{current_user.email}')"}, 200



    @token_required
    def get(self, current_user):

        """Get user records"""

        records = models.Record.query.filter_by(user_id=current_user.id).all()

        if len(records) == 0:
            return {"message": f"User '{current_user.email}' has no records"}, 404

        
        return [marshal(record, RECORD_RESOURCE_FIELDS) for record in records], 200
