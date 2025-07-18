"""
File for storing constants used across the application.
Import this file as `import app.constants as const`
"""


class HTTPStatus:
    # HTTP status codes
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500


class Timeouts:
    # Time constants
    SESSION_TOKEN = 3600  # 1 hour in seconds
    REDIS_CACHE = 1800  # 30 minutes in seconds
