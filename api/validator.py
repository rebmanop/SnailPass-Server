from api import IV_AND_DATA_DELIMETER
from api.errors import APIDataFormatError

class Validator():
    def __init__(self, args: dict):
        self.data = args.copy()
        self.data.pop("id")
 
    def validate_data_format(self) -> None:
        wrong_format_args = []

        for key, value in self.data.items(): 
            value_tokens = value.split(IV_AND_DATA_DELIMETER)
            if len(value_tokens) != 2:
                wrong_format_args.append(key)
                
        if len(wrong_format_args) > 0:        
            raise APIDataFormatError(f"Some arguments are in wrong format: {wrong_format_args}")
        
