from enum import Enum

class StatusCodeEnum(Enum):
    # Success Codes (2xx)
    SUCCESS = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    PERMANENT_REDIRECT = 301

    # Client Error Codes (4xx)
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    VALIDATION_ERROR = 422
    TOO_MANY_REQUESTS = 429

    # Server Error Codes (5xx)
    INTERNAL_ERROR = 500
    NOT_IMPLEMENTED = 501
    SERVICE_UNAVAILABLE = 503