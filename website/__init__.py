from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from configparser import ConfigParser


db = SQLAlchemy()
DB_NAME = "database.db"
UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
ALLOWED_MIME_TYPE = {'image/png', 'image/jpeg', 'image/gif', 'image/svg+xml'}

app = Flask(__name__)

def create_app(config: ConfigParser):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config['WEBSITE']['secretKey']
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config["SESSION_COOKIE_HTTPONLY"] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)
    

    from .models import User
    from .init_defaults import init_defaults, create_roles
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    
    with app.app_context():
        db.create_all()
        create_roles()
        init_defaults(config['ADMIN']['username'], config['ADMIN']['password'])


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
