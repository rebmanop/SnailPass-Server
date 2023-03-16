from api import IV_AND_DATA_DELIMETER
from api.errors import APIDataFormatError
from api.core import WRONG_FORMAT_ARGUMENT_RESPONSE, EMPTY_STRING_ARGUMENT_RESPONSE


class Validator:
    def __init__(
        self,
        not_encrypted_args: list = None,
        all_not_encrypted: bool = False,
        empty_string_allowed: list = None,
    ):
        self.not_encrypted_args = []
        self.empty_string_allowed = []
        self.all_not_encrypted = all_not_encrypted

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

    def validate_args(self, args: dict) -> None:

        wrong_format_args = {}

        self.__check_for_empty_string(args, wrong_format_args)
        if self.all_not_encrypted == False:
            self.__check_for_correct_format(args, wrong_format_args)

        if len(wrong_format_args) > 0:
            raise APIDataFormatError(wrong_format_args)
