from .models import Role
from flask_login import current_user
from flask import Response

def admin_required(function):
    def wrapper_admin(*args, **kwargs):
        if current_user.role != 0:
            return Response(status=403)
        return function(*args, **kwargs)
    wrapper_admin.__name__ = function.__name__
    return wrapper_admin

def user_required(function):
    def wrapper_user(*args, **kwargs):
        if current_user.role != 1:
            return Response(status=403)
        return function(*args, **kwargs)
    wrapper_user.__name__ = function.__name__
    return wrapper_user
