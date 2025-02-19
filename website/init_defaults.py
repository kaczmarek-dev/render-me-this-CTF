from . import db
from .models import User
from werkzeug.security import generate_password_hash

def init_defaults():
    """Pre-Populate User Table"""
    if User.query.first() is None:
        new_user = User(
                username="admin",
                is_admin=True, 
                password=generate_password_hash("admin", method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()