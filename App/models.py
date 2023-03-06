from flask_sqlalchemy import SQLAlchemy
import logging as lg
from flask_login import UserMixin
from App import db





class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    firstname = db.Column(db.String(1000))
    address = db.Column(db.String(1000))
    country = db.Column(db.String(1000))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    Orders = db.relationship('Order', backref='user', lazy=True)


# class Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
#     title = db.Column(db.String(100), unique=True)
#     category = db.Column(db.String(100))
#     description = db.Column(db.String(1000))
#     price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
#     image = db.Colummn(db.BLOB)

# class Purchased_item(db.Model):
#     id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
#     size = db.Column(db.String(100), unique=True)
#     item_status = db.Column(db.String(100)) #status for each item
#     color = db.Column(db.String(100))
#     # "fk item id and order id"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    item_quantity = db.Column(db.Integer, unique=True)
    order_status = db.Column(db.String(100)) #status for all items
    total_price = db.Column(db.String(1000))
    user_email = db.Column(db.String(100), db.ForeignKey('user.email'),
        nullable=False)





