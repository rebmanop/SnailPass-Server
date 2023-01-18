import models
from models import db
from flask_restful import Resource, reqparse, fields, marshal, request
from api.access_restrictions import token_required


additional_field_resource_fields = {
                        'id': fields.String, 
                        'field_name': fields.String,
                        'value': fields.String,
                        'record_id': fields.String,
                        'nonce': fields.String
                        }


class AdditionalField(Resource):
    @token_required
    def post(self, current_user):
        
        """Create new additional field"""

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Additional field id is required", required=True)
        parser.add_argument("field_name", type=str, help="Additional field name is required", required=True)
        parser.add_argument("value", type=str, help="Additional field value is required", required=True)
        parser.add_argument("record_id", type=str, help="Additional field's record id is required", required=True)
        parser.add_argument("nonce", type=str, help="Additional field's nonce is required", required=True)


        args = parser.parse_args()
        record_with_recived_record_id = models.Record.query.get(args["record_id"])

        if not record_with_recived_record_id:
            return {"message": f"Record with recived record id doesn't exist"}, 404
        elif current_user.id != record_with_recived_record_id.user_id:
            return {"message": f"Record with id {record_with_recived_record_id.id} doesn't belong to the current user"}, 403
        elif models.AdditionalField.query.get(args["id"]):
            return {"message": f"Additional field with id '{args['id']}' already exist"}, 409
        elif models.AdditionalField.query.filter_by(record_id=record_with_recived_record_id.id, field_name=args["field_name"]).all():
            return {"message": f"Additional field with name '{args['field_name']}' already exist in this record"}, 409
    

        additional_field = models.AdditionalField(id=args["id"], field_name=args["field_name"], value=args["value"], 
                                record_id=record_with_recived_record_id.id, nonce=args["nonce"])


        db.session.add(additional_field)
        db.session.commit()

        return {"message": f"Additional record field '{args['field_name']}' created successfully (record_name = '{record_with_recived_record_id.name}',  user = '{current_user.email}')"}, 201
    
    
    @token_required
    def delete(self, current_user):

        "Delete additional field"

        af_id = request.args.get("id")

        if not af_id:
            return {"message": f"Additional field id is missing in uri args"}, 400

        additional_field = models.AdditionalField.query.get(af_id)
       
        if not additional_field:
            return {"message": f"Additional field with id '{af_id}' doesn't exist"}, 404


        db.session.delete(additional_field)
        db.session.commit()

        return {"message": f"Additional field '{additional_field.field_name}' deleted successfully (user = '{current_user.email}')"}, 200
        

    @token_required
    def patch(self, current_user):

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Additional field's id is required", required=True)
        parser.add_argument("field_name", type=str,  type=str, help="Additional field's name is required", required=True)
        parser.add_argument("value", type=str,  type=str, help="Additional field's value is required", required=True)
        parser.add_argument("record_id", type=str, help="Additional field's record id is required", required=True)
        parser.add_argument("nonce", type=str, help="Additional field's nonce is required", required=True)
        
        args = parser.parse_args()

        additional_field = models.AdditionalField.query.get(args["id"])
        record_with_recived_record_id = models.Record.query.get(args["record_id"])


        if not additional_field:
            return {"message": f"Additional field with id '{args['id']}' doesn't exist "}, 404
        elif not record_with_recived_record_id:
            return {"message": f"Record with id '{record_with_recived_record_id.id}' doesn't exist "}, 404
        elif current_user.id != record_with_recived_record_id.user_id:
            return {"message": f"Record with id '{record_with_recived_record_id.id}' doesn't belong to the current user"}, 403
        elif record_with_recived_record_id.id != additional_field.record_id:
            return {"message": f"Additional field with id '{additional_field.id}' doesn't belong to the record with id '{record_with_recived_record_id.id}'"}, 409


        if db.session.query(models.AdditionalField).filter(AdditionalField.record_id == additional_field.record_id,
                                                           AdditionalField.name == args["field_name"], 
                                                           AdditionalField.id != additional_field.id): 
            
            return {"message": f"Additional field with name '{args['field_name']}' already exists in record with id '{additional_field.record_id}' (user = '{current_user.email}')"}, 409
        
        if additional_field.record_id != args["record_id"]:
            return {"message": f"Record id of an existing additional field can't be changed"}, 400

        additional_field.field_name = args["field_name"]
        additional_field.value = args["value"]
        additional_field.nonce = args["nonce"]

        
        db.session.commit()
        return {"message": f"Changes for the additional field '{args['id']}' were successfully made"}, 200


       



    @token_required
    def get(self, current_user):

        """Get additional fields by record id"""

        record_id = request.args.get("id")

        if not record_id:
            return {"message": f"Record id is missing in uri args"}, 400

        record_with_recived_record_id = models.Record.query.get(record_id)

        if not record_with_recived_record_id:
            return {"message": f"Record with id '{record_with_recived_record_id.id}' doesn't exist "}, 404
        elif current_user.id != record_with_recived_record_id.user_id:
            return {"message": f"Record with id '{record_with_recived_record_id.id}' doesn't belong to the current user"}, 403

        record_additional_fields = models.AdditionalField.query.filter_by(record_id=record_with_recived_record_id.id).all()

        if len(record_additional_fields) == 0:
            return {"message": f"Record with id '{record_with_recived_record_id.id}' has no additional fields"}, 404

        
        return [marshal(additional_field, additional_field_resource_fields) for additional_field in record_additional_fields], 200