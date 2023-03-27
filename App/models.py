from flask_sqlalchemy import SQLAlchemy
import logging as lg
from flask_login import UserMixin
from App import db





class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)# primary keys are required by SQLAlchemy
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    firstname = db.Column(db.String(1000))
    address = db.Column(db.String(1000))
    country = db.Column(db.String(1000))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    Orders = db.relationship('Order', backref='user', lazy=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    title = db.Column(db.String(100))
    category = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    image = db.Column(db.LargeBinary)

class Purchased_item(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    size = db.Column(db.String(100))
    item_status = db.Column(db.String(100)) #status for each item
    color = db.Column(db.String(100))
    # "fk item id and order id"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    item_quantity = db.Column(db.Integer)
    order_status = db.Column(db.String(100)) #status for all items
    total_price = db.Column(db.String(1000))
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'),
        nullable=False)



# class Basket(db.Model):
    

