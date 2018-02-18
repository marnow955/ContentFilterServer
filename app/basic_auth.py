import hashlib
from functools import wraps
from flask import request, Response
from typing import List
from .config import AuthConfig


auth_config = AuthConfig


def configure_auth(config: List[dict] = None):
    if config:
        global auth_config
        auth_config = config


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    for user in auth_config:
        hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
        if username == user['USER'] and hashed_password.lower() == user['PASSWORD'].lower():
            return True
    return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
