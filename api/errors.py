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


class APIResourceNotFoundError(APIError):
    """Custom Resource Not Found Error Class"""
    code = 404
    description = "Resource Not Found"


class APIMissingParameterError(APIError):
    """Custom Missing Parameter Error Class"""
    code = 400
    description = "Missing Parameter"


class APIMissingRequestHeaderError(APIError):
    """Custom Missing Header Error Class"""
    code = 400
    description = "Missing Request Header"






