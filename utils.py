from functools import wraps
from flask_jwt_extended import verify_jwt_in_request


def jwt_required_route(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return route(*args, **kwargs)

    return wrapper
