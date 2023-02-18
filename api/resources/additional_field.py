import models
from models import db
import api.errors as err
from nameof import nameof
from api.validator import Validator
from flask_restful import Resource, reqparse, marshal, request
from api.access_restrictions import token_required
from api.resource_fields import ADDITIONAL_FIELD_RESOURCE_FIELDS
from api.core import create_successful_response
from api.core import MISSING_ARGUMENT_RESPONSE


class AdditionalField(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument(
            nameof(models.AdditionalField.id),
            type=str,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.parser.add_argument(
            nameof(models.AdditionalField.name),
            type=str,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.parser.add_argument(
            nameof(models.AdditionalField.value),
            type=str,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.parser.add_argument(
            nameof(models.AdditionalField.record_id),
            type=str,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.validator = Validator(
            not_encrypted_args=[
                nameof(models.AdditionalField.id),
                nameof(models.AdditionalField.record_id),
            ]
        )

    @token_required
    def post(self, current_user):
        """Create new additional field"""

        args = self.parser.parse_args()
        self.validator.validate_args(args)
        new_afs_record = db.session.query(models.Record).get(
            args[nameof(models.AdditionalField.record_id)]
        )

        if not new_afs_record:
            raise err.APIResourceNotFoundError(
                f"Record with id {args[nameof(models.AdditionalField.record_id)]} doesn't exist"
            )

        if current_user.id != new_afs_record.user_id:
            raise err.APIAccessDeniedError(
                f"Record {new_afs_record.id} doesn't belong to the current user {current_user.id}"
            )

        if db.session.query(models.AdditionalField).get(
            args[nameof(models.AdditionalField.id)]
        ):
            raise err.APIResourceAlreadyExistsError(
                f"Additional field with id {args[nameof(models.AdditionalField.id)]} already exists"
            )

        additional_field = models.AdditionalField(
            id=args[nameof(models.AdditionalField.id)],
            name=args[nameof(models.AdditionalField.name)],
            value=args[nameof(models.AdditionalField.value)],
            record_id=new_afs_record.id,
        )

        db.session.add(additional_field)
        db.session.commit()

        return create_successful_response(
            f"Additional field {additional_field.id} created", 201
        )

    @token_required
    def delete(self, current_user):
        "Delete additional field"

        af_id = request.args.get(nameof(models.AdditionalField.id))

        if not af_id:
            raise err.APIMissingParameterError(
                f"Additional field id is missing in URI arguments"
            )

        additional_field = db.session.query(models.AdditionalField).get(af_id)

        if not additional_field:
            raise err.APIResourceNotFoundError(
                f"Additional field with id {af_id} doesn't exist"
            )

        if additional_field.record.user_id != current_user.id:
            raise err.APIAccessDeniedError(
                f"Additional field {additional_field.id} doesn't belong to the current user {current_user.id}"
            )

        db.session.delete(additional_field)
        db.session.commit()

        return create_successful_response(
            f"Additional field {additional_field.id} deleted successfully", 200
        )

    @token_required
    def put(self, current_user):
        """Edit existing additional field"""

        args = self.parser.parse_args()
        self.validator.validate_args(args)
        additional_field = db.session.query(models.AdditionalField).get(
            args[nameof(models.AdditionalField.id)]
        )

        if not additional_field:
            raise err.APIResourceNotFoundError(
                f"Additional field with id {args[nameof(models.AdditionalField.id)]} doesn't exist"
            )

        if additional_field.record.user_id != current_user.id:
            raise err.APIAccessDeniedError(
                f"Additional field {additional_field.id} doesn't belong to the current user {current_user.id}"
            )

        additional_field.name = args[nameof(models.AdditionalField.name)]
        additional_field.value = args[nameof(models.AdditionalField.value)]

        db.session.commit()
        return create_successful_response(
            f"Additional field {additional_field.id} changed successfully", 200
        )

    @token_required
    def get(self, current_user):
        """Get additional fields by record id"""

        record_id = request.args.get(nameof(models.Record.id))

        if not record_id:
            raise err.APIMissingParameterError(f"Record id is missing in URI arguments")

        record = db.session.query(models.Record).get(record_id)

        if not record:
            raise err.APIResourceNotFoundError(
                f"Record with id {record_id} doesn't exist"
            )
        elif current_user.id != record.user_id:
            raise err.APIAccessDeniedError(
                f"Record {record.id} doesn't belong to the current user {current_user.id}"
            )

        if len(record.additional_fields) == 0:
            raise err.APIResourceNotFoundError(
                f"Current user's {current_user.id} record {record.id}  has no additional fields"
            )
        else:
            return [
                marshal(additional_field, ADDITIONAL_FIELD_RESOURCE_FIELDS)
                for additional_field in record.additional_fields
            ], 200
