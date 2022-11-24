import models
import datetime
from api import db
from flask_restful import Resource, marshal_with, reqparse
from api.access_restrictions import token_required
from flask_restful import Resource, reqparse, request, fields, marshal_with

record_resource_fields = {
                        'id': fields.String, 
                        'name': fields.String,
                        'login': fields.String,
                        'encrypted_password': fields.String,
                        'user_id': fields.String,
                        'is_favorite': fields.Boolean,
                        'is_deleted': fields.Boolean,
                        'creation_time': fields.DateTime,
                        'update_time': fields.DateTime,
                        'nonce': fields.String
                        }


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
            return {"message": f"Record with id '{args['id']}' already exist "}, 409
        elif models.Record.query.filter_by(user_id=current_user.id, name=args["name"]).all():
            return {"message": f"Record with name '{args['name']}' already exist "}, 409


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
        parser.add_argument("name", type=str)
        parser.add_argument("login", type=str)
        parser.add_argument("encrypted_password", type=str)
        args = parser.parse_args()

        record = models.Record.query.get(args["id"])

        if not record:
            return {"message": f"Record with id '{args['id']}' doesn't exist "}, 404
        
        if current_user.id != record.user_id:
            return {"message": "You dont have access rights to edit this record"}, 403

        record_changed = False
        
        if args["name"]:
            record.name = args["name"]
            record_changed = True

        
        if args["login"]:
            record.login = args["login"]
            record_changed = True

        
        if args["encrypted_password"]:
            record.encrypted_password = args["encrypted_password"]
            record_changed = True


        if record_changed:
            record.update_time = datetime.datetime.now()
            db.session.commit()
            return {"message": f"Changes for the record '{args['id']}' were successfully made"}, 200
        else:
            return {"message": f"Changes for the record '{args['id']}' weren't made because request body is empty"}, 400 

    
    @token_required
    def delete(self, current_user):

        "Delete record"

        record_id = request.args.get("id")

        if not record_id:
            {"message": "Record id not found in the url params"}, 400

        record = models.Record.query.get(record_id)
        additional_fields = models.AdditionalField.query.filter_by(record_id=record_id).all()

        if record == None:
            return {"message": "Record with that id doesn't exist"}, 404

        if current_user.id != record.user_id:
            return {"message": "You dont have access rights to delete this record"}, 403

        
        if len(additional_fields) != 0:
            for field in additional_fields:
                db.session.delete(field)
        
        db.session.delete(record)
        db.session.commit()

        return {"message": f"Record '{record.name}' deleted successfully (user = '{current_user.email}')"}, 200



    @token_required
    @marshal_with(record_resource_fields)
    def get(self, current_user):

        """Get user records"""

        records = models.Record.query.filter_by(user_id=current_user.id).all()

        if len(records) == 0:
            return {"message": f"User '{current_user.email}' has no records"}

        return records, 200
