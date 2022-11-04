import models
import datetime
from api import db
from flask_restful import Resource, marshal_with, reqparse
from api.access_restrictions import admin_only_function, token_required
from flask_restful import Resource, reqparse, request, fields, marshal_with

record_resource_fields = {
                        'id': fields.String, 
                        'name': fields.String,
                        'login': fields.String,
                        'encrypted_password': fields.String,
                        'user_id': fields.String,
                        'is_favorite': fields.Boolean,
                        'is_deleted': fields.Boolean,
                        'creation_time': fields.DateTime
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
        args = parser.parse_args()


        if models.Record.query.get(args["id"]):
            return {"message": f"Record with id '{args['id']}' already exist "}, 409
        elif models.Record.query.filter_by(name=args["name"]).all():
            return {"message": f"Record with name '{args['name']}' already exist "}, 409


        record = models.Record(id=args["id"], name=args["name"], login=args["login"], 
                                encrypted_password=args["encrypted_password"], user_id=current_user.id, creation_time=datetime.datetime.now())

        db.session.add(record)
        db.session.commit()

        return {"message": f"Record '{args['name']}' created successfully (user = '{current_user.email}')"}, 201
    
    
    @token_required
    def delete(self, current_user):

        "Delete record"

        record_id = request.args.get("id")

        if not record_id:
            {"message": "Record id not found in the url params"}, 400

        record = models.Record.query.get(record_id)

        if record == None:
            return {"message": "Record with that id doesn't exist"}, 404

        if current_user.id != record.user_id:
            return {"message": "You dont have access rights to delete this record"}, 403
        
        db.session.delete(record)
        db.session.commit()

        return {"message": f"Record '{record.name}' deleted successfully (user = '{current_user.email}')"}, 200


    @admin_only_function
    @marshal_with(record_resource_fields)
    def get(self):
        
        """Get all records"""

        records = models.Record.query.all()

        if len(records) == 0:
            return {"message": "No records in the database"}, 404

        return records, 200