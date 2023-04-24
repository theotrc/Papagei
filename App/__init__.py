from asyncio.log import logger
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from flask_mail import  Mail
#test

db = SQLAlchemy()
def create_app():
    app=Flask(__name__)
    app.config.from_object('config')
    app.config['UPLOAD_FOLDER'] = 'static/files'
    
    # Create database connection object
    



    from .routes.home import home_blueprint
    from .routes.news import news_blue
    from .routes.account import account_blue
    from .routes.contact import contact_blue
    from .routes.auth import auth_blue
    from .routes.admin import admin
    from .routes.sale import sale_blue
    from .routes.basket import basket_blue

    app.register_blueprint(home_blueprint)
    app.register_blueprint(news_blue)
    app.register_blueprint(account_blue)
    app.register_blueprint(contact_blue)
    app.register_blueprint(auth_blue)
    app.register_blueprint(admin)
    app.register_blueprint(sale_blue)
    app.register_blueprint(basket_blue)

    return app


app = create_app()
mail = Mail(app)

with app.app_context():
    db.init_app(app)
    db.create_all()




login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# logger = logging.getLogger("monlog")
# logger.setLevel(logging.DEBUG)
# fh = logging.FileHandler('logs.log')
# fh.setLevel(logging.DEBUG)
# formatter =logging.Formatter("%(levelname)-8s %(asctime)s %(message)s")
# fh.setFormatter(formatter)
# logger.addHandler(fh)

from App import models

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return models.User.query.get(int(user_id))


@app.cli.command("init_db")
def init_db():
    models.init_db()

