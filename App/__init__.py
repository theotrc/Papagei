from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import stripe_keys
import stripe
import os
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app=Flask(__name__)
    app.config.from_object('config')
    app.config['UPLOAD_FOLDER'] = 'static/files'
    
    # Create database connection object
    

    from .routes.order import order_blue
    from .routes.mention import mention_blue
    from .routes.home import home_blueprint
    from .routes.news import news_blue
    from .routes.account import account_blue
    from .routes.contact import contact_blue
    from .routes.auth import auth_blue
    from .routes.admin import admin
    from .routes.sale import sale_blue
    from .routes.basket import basket_blue
    from .routes.papagei import papagei_blue
    from .routes.checkout import checkout_blue

    app.register_blueprint(order_blue)
    app.register_blueprint(mention_blue)
    app.register_blueprint(checkout_blue)
    app.register_blueprint(papagei_blue)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(news_blue)
    app.register_blueprint(account_blue)
    app.register_blueprint(contact_blue)
    app.register_blueprint(auth_blue)
    app.register_blueprint(admin)
    app.register_blueprint(sale_blue)
    app.register_blueprint(basket_blue)

    return app
stripe_public_key= stripe_keys['publishable_key']
stripe.api_key = stripe_keys['secret_key']
pwd =os.environ.get('MAIL_MDP')
email_sender = os.environ.get('MAIL_SENDER')
app = create_app()

with app.app_context():
    db.init_app(app)
    migrate.init_app(app, db)
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

