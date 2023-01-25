import models
from models import db
from flask_restful import Resource, reqparse, marshal, request
from api.access_restrictions import token_required
from api.resource_fields import ADDITIONAL_FIELD_RESOURCE_FIELDS
from api.utils import non_empty_string


class AdditionalField(Resource):
    @token_required
    def post(self, current_user):
        
        """Create new additional field"""

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=non_empty_string, help="Additional field id is missing at all, value is null or value is empty", required=True, nullable=False)
        parser.add_argument("field_name", type=non_empty_string, help="Additional field name is missing at all, value is null or value is empty", required=True, nullable=False)
        parser.add_argument("value", type=non_empty_string, help="Additional field value is missing at all, value is null or value is empty", required=True, nullable=False)
        parser.add_argument("record_id", type=non_empty_string, help="Additional field's record id is missing at all, value is null or value is empty", required=True, nullable=False)

        args = parser.parse_args()
        record_with_recived_record_id = db.session.query(models.Record).get(args["record_id"])


        if not record_with_recived_record_id:
            return {"message": f"Record with recived record id doesn't exist"}, 404
        elif current_user.id != record_with_recived_record_id.user_id:
            return {"message": f"Record with id {record_with_recived_record_id.id} doesn't belong to the current user"}, 403
        elif db.session.query(models.AdditionalField).get(args["id"]):
            return {"message": f"Additional field with id '{args['id']}' already exist"}, 409
        elif db.session.query(models.AdditionalField).filter_by(record_id=record_with_recived_record_id.id, field_name=args["field_name"]).all():
            return {"message": f"Additional field with name '{args['field_name']}' already exist in this record"}, 409
    

        additional_field = models.AdditionalField(id=args["id"], field_name=args["field_name"], value=args["value"], 
                                record_id=record_with_recived_record_id.id)


        db.session.add(additional_field)
        db.session.commit()

        return {"message": f"Additional record field '{args['field_name']}' created successfully (record_name = '{record_with_recived_record_id.name}',  user = '{current_user.email}')"}, 201
    
    
    @token_required
    def delete(self, current_user):

        "Delete additional field"

        af_id = request.args.get("id")

        if not af_id:
            return {"message": f"Additional field id is missing in uri args"}, 400

        additional_field = db.session.query(models.AdditionalField).get(af_id)
       
        if not additional_field:
            return {"message": f"Additional field with id '{af_id}' doesn't exist"}, 404


        db.session.delete(additional_field)
        db.session.commit()

        return {"message": f"Additional field '{additional_field.field_name}' deleted successfully (user = '{current_user.email}')"}, 200
        

    @token_required
    def patch(self, current_user):

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=non_empty_string, help="Additional field's id is missing at all, value is null or value is empty", required=True, nullable=False)
        parser.add_argument("field_name", type=non_empty_string, help="Additional field's name is missing at all, value is null or value is empty", required=True, nullable=False)
        parser.add_argument("value", type=non_empty_string, help="Additional field's value is missing at all, value is null or value is empty", required=True, nullable=False)
        parser.add_argument("record_id", type=non_empty_string, help="Additional field's record id is missing at all, value is null or value is empty", required=True, nullable=False)
        
        args = parser.parse_args()

        additional_field = db.session.query(models.AdditionalField).get(args["id"])
        record_with_recived_record_id = db.session.query(models.Record).get(args["record_id"])


        if not additional_field:
            return {"message": f"Additional field with id '{args['id']}' doesn't exist "}, 404
        elif not record_with_recived_record_id:
            return {"message": f"Record with id '{args['record_id']}' doesn't exist"}, 404
        elif current_user.id != record_with_recived_record_id.user_id:
            return {"message": f"Record with id '{args['record_id']}' doesn't belong to the current user"}, 403
        elif args['record_id'] != additional_field.record_id:
            return {"message": f"Additional field with id '{additional_field.id}' doesn't belong to the record with id '{args['record_id']}'"}, 409


        if db.session.query(models.AdditionalField).filter(models.AdditionalField.record_id == additional_field.record_id,
                                                           models.AdditionalField.field_name == args["field_name"], 
                                                           models.AdditionalField.id != additional_field.id).first(): 
            return {"message": f"Additional field with name '{args['field_name']}' already exists in record with id '{additional_field.record_id}' (user = '{current_user.email}')"}, 409
        

        additional_field.field_name = args["field_name"]
        additional_field.value = args["value"]

        
        db.session.commit()
        return {"message": f"Changes for the additional field '{args['id']}' were successfully made"}, 200


    @token_required
    def get(self, current_user):

        """Get additional fields by record id"""

        record_id = request.args.get("id")

        if not record_id:
            return {"message": f"Record id is missing in uri args"}, 400

        record = db.session.query(models.Record).get(record_id)

        if not record:
            return {"message": f"Record with id '{record_id}' doesn't exist "}, 404
        elif current_user.id != record.user_id:
            return {"message": f"Record with id '{record_id}' doesn't belong to the current user"}, 403

        if len(record.additional_fields) == 0:
            return {"message": f"Record with id '{record_id}' has no additional fields"}, 404
        else:
            return [marshal(additional_field, ADDITIONAL_FIELD_RESOURCE_FIELDS) for additional_field in record.additional_fields], 200


        