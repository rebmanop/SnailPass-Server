import models
from api import db
from flask_restful import Resource, reqparse
from api.access_restrictions import token_required

class AdditionalField(Resource):
    @token_required
    def post(self, current_user):
        
        """Create new additional field"""

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Additional field id is required", required=True)
        parser.add_argument("field_name", type=str, help="Additional field id is required", required=True)
        parser.add_argument("value", type=str, help="Additional field id is required", required=True)
        parser.add_argument("record_id", type=str, help="Additional field id is required", required=True)

        args = parser.parse_args()

        additional_field = models.AdditionalField(id=args["id"], field_name=args["field_name"], value=args["value"], 
                                record_id=args["record_id"])

        record = models.Record.query.get(args["record_id"])

        db.session.add(additional_field)
        db.session.commit()

        return {"message": f"Additional record field '{args['field_name']}' created successfully (record_name = '{record.name}',  user = '{current_user.email}')"}, 201
    
    
    @token_required
    def delete(self, current_user):

        "Delete additional field"

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Additional field id is required", required=True)

        args = parser.parse_args()

        additional_field = models.AdditionalField.query.filter_by(id=args["id"]).all()
        db.session.delete(additional_field)
        db.session.commit()

        record = models.Record.query.get(additional_field.record_id)


        return {"message": f"Additional record field '{additional_field.field_name}' deleted successfully (record_name = '{record.name}',  user = '{current_user.email}')"}, 200
        