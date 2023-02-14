from api import IV_AND_DATA_DELIMETER
from api.errors import APIDataFormatError

class Validator():
    def __init__(self, args: dict, exclude_from_validation=None):
        self.data = args.copy()
        if exclude_from_validation:
            for arg_to_exclude in exclude_from_validation:
                self.data.pop(arg_to_exclude)
 
    def validate_data_format(self) -> None:
        wrong_format_args = []

        for key, value in self.data.items(): 
            value_tokens = value.split(IV_AND_DATA_DELIMETER)
            if len(value_tokens) != 2:
                wrong_format_args.append(key)
                
        if len(wrong_format_args) > 0:        
            raise APIDataFormatError(wrong_format_args)
        
