class APIError(Exception):
    """All custom API Exceptions"""

    code = 0
    description = "Base API Error"


class APIAuthError(APIError):
    """Custom Authentication Error Class."""

    code = 401
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


class APIResourceAlreadyExistsError(APIError):
    """Custom Resource Already Exists Error Class"""

    code = 409
    description = "Resource Already Exists"


class APIAccessDeniedError(APIError):
    """Custom Access Denied Error"""

    code = 403
    description = "Access Denied"


class APIUnprocessableEntityError(APIError):
    """Custom Unprocessable Entity Error"""

    code = 422
    description = "Unprocessable Entity"
