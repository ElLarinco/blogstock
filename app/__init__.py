from flask import Flask, render_template
from flask_login import current_user
from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "blogstock.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")

    from .models import User
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html", user=current_user), 404

    return app

def create_database(app):
    if not path.exists("/app" + DB_NAME):
        db.create_all(app=app)