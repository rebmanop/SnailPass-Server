class APIError(Exception):
    """All custom API Exceptions"""
    pass


class APIAuthError(APIError):
    """Custom Authentication Error Class."""
    code = 403
    description = "Authentication Error"


class APIDataFormatError(APIError):
    """Custom Data Format Error Class"""
    code = 400
    description = "Data Format Error"



