from flask import Flask
from database import Database
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import User

from app import auth, main

import config

# init Database so we can use it later in our models
db = Database('data/db.csv', "https://yadi.sk/d/nC4boLtXg5CyeA", "sqlite:///ecg.sqlite", create_new=config.reset_db)


def create_app():
    app = Flask(__name__, static_url_path="/static", template_folder='../templates', static_folder='../static')

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # u = DBUsers.query.get(id)
        return User(user_id, 100, True)

    from app.auth.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from app.main.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app