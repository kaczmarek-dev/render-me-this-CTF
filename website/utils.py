from .models import Role
from flask_login import current_user
from flask import Response

def admin_required(function):
    def decorator(*args, **kwargs):
        print(current_user.role)
        if current_user.role != 0:
            return Response(status=403)
        return function(*args, **kwargs)
    return decorator
