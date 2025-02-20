from . import db
from .models import User, Role
from werkzeug.security import generate_password_hash

def init_defaults():
    """Pre-Populate User Table"""
    if User.query.first() is None:
        admin = User(
            username="admin",
            password=generate_password_hash("admin", method='pbkdf2:sha256'),
            role=0
            )
        db.session.add(admin)
        db.session.commit()

        user = User(
            username="user",
            password=generate_password_hash("user", method='pbkdf2:sha256'),
            role=1
            )
        db.session.add(user)
        db.session.commit()
        print("Admin created successfully!")

def create_roles():
    if Role.query.first() is None:
        admin = Role(id=0, name='Admin')
        user = Role(id=1, name='User')

        db.session.add(admin)
        db.session.add(user)

        db.session.commit()
        print("Roles created successfully!")
