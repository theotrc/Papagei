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

    ## reset token for reset password
    reset_token = db.Column(db.String(100))
    reset_token_expiry = db.Column(db.DateTime)

    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    Carts = db.relationship('Cart', backref='user', lazy=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    title = db.Column(db.String(100))
    category = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    image = db.Column(db.LargeBinary)
    Orders = db.relationship('Cart_item', backref='item', lazy="joined")

# class Purchased_item(db.Model):
#     id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
#     size = db.Column(db.String(100))
#     item_status = db.Column(db.String(100)) #status for each item
#     color = db.Column(db.String(100))
#     #  "fk item id and order id"

class Cart_item(db.Model):
    """item_quantity (Int) | order_status (String) | cart_item_id (Int) | item_id (Int)"""

    ##unique ID
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    ##quantité de l'item
    item_quantity = db.Column(db.Integer)
    
    ##status de la commande 
    order_status = db.Column(db.String(100)) #status for all items

    ##size
    size = db.Column(db.String(100))


    cart_item_id = db.Column(db.Integer, db.ForeignKey('cart.id'),
        nullable=False)
    
    ##ID de l'article
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'),
        nullable=False)
    


class Cart(db.Model):
    """user_id (int): Unique id of user | 
        total_price (float): default: 0"""
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy

    ##id du client 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    
    total_price = db.Column(db.Float, nullable=False, default=0)

    
    cart_items = db.relationship('Cart_item', backref='cart', lazy=True)
    


    

