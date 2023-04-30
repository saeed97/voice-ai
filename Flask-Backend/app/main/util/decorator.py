from functools import wraps

from flask import request

from app.main.service.user.auth_helper import Auth
from typing import Callable
import logging

log = logging.getLogger(__name__)

def token_required(f) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated

def validate_result(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args,**kwargs):
        value = {"Fail", "ERROR: validation response!!"}
        try:
            value = f(*args,*kwargs)
        except AttributeError as e:
            log.error(f"ERROR: can not find the expected response from the API: {e}!!")
        return value
    return decorated