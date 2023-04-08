from api import IV_AND_DATA_DELIMETER
from api.errors import APIDataFormatError
from api.core import (
    WRONG_FORMAT_ARGUMENT_RESPONSE,
    EMPTY_STRING_ARGUMENT_RESPONSE,
    EMAIL_NOT_VALID,
)
from email_validator import validate_email, EmailNotValidError


class Validator:
    def __init__(
        self,
        not_encrypted_args: list = None,
        all_not_encrypted: bool = False,
        empty_string_allowed: list = None,
        email_validation=False,
    ):
        self.not_encrypted_args = []
        self.empty_string_allowed = []
        self.all_not_encrypted = all_not_encrypted
        self.email_validation = email_validation

        if not_encrypted_args:
            self.not_encrypted_args = not_encrypted_args

        if empty_string_allowed:
            self.empty_string_allowed = empty_string_allowed

    def __check_for_empty_string(self, args: dict, wrong_format_args: dict) -> None:
        for key, value in args.items():
            if value == "" and key not in wrong_format_args:
                if key not in self.empty_string_allowed:
                    wrong_format_args[key] = EMPTY_STRING_ARGUMENT_RESPONSE

    def __check_for_correct_format(self, args: dict, wrong_format_args: dict) -> None:
        for key, value in args.items():
            if key not in self.not_encrypted_args and key not in wrong_format_args:
                value_tokens = value.split(IV_AND_DATA_DELIMETER)
                if len(value_tokens) != 2:
                    wrong_format_args[key] = WRONG_FORMAT_ARGUMENT_RESPONSE

    def __validate_email(self, args: dict, wrong_format_args: dict) -> None:
        try:
            validate_email(args["email"])
        except EmailNotValidError:
            if "email" not in wrong_format_args:
                wrong_format_args["email"] = EMAIL_NOT_VALID

    def validate_args(self, args: dict) -> None:
        wrong_format_args = {}

        self.__check_for_empty_string(args, wrong_format_args)
        if self.all_not_encrypted == False:
            self.__check_for_correct_format(args, wrong_format_args)

        if self.email_validation == True:
            self.__validate_email(args, wrong_format_args)

        if len(wrong_format_args) > 0:
            raise APIDataFormatError(wrong_format_args)
