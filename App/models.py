from flask_sqlalchemy import SQLAlchemy
import logging as lg
from flask_login import UserMixin
from App import db



class User(UserMixin,db.Model):

    id = db.Column(db.Integer, primary_key=True) 

    email = db.Column(db.String(100), unique=True)
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

    order = db.relationship('Order', backref='user', lazy=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)


    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    composition = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.LargeBinary)
    color= db.Column(db.String(100))

    price = db.Column(db.Float, nullable=False)

    quantity =db.Column(db.Integer)

    weight = db.Column(db.Float, nullable=False)
    
    images = db.relationship('ItemImage', backref='item', lazy="joined")

    Orders = db.relationship('Cart_item', backref='item', lazy="joined")

class ItemImage(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    
    image = db.Column(db.LargeBinary)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'),
        nullable=False)


class Cart_item(db.Model):
    """item_quantity (Int) | order_status (String) | cart_item_id (Int) | item_id (Int)"""

    ##unique ID
    id = db.Column(db.Integer, primary_key=True)
    ##quantité de l'item
    item_quantity = db.Column(db.Integer)
    
    ##size
    size = db.Column(db.String(100))


    cart_item_id = db.Column(db.Integer, db.ForeignKey('cart.id'),
        nullable=False)
    
    ##ID de l'article
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'),
        nullable=False)
    


class Cart(db.Model):

    id = db.Column(db.Integer, primary_key=True)


    expedition_price = db.Column(db.Float, nullable=False, default=0)
    
    price = db.Column(db.Float, nullable=False, default=0)

    cart_weight = db.Column(db.Float, nullable=False, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

    cart_items = db.relationship('Cart_item', backref='cart', lazy=True)
    
    order = db.relationship('Order', backref='cart', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    facture =db.Column(db.LargeBinary)
    
    status =  db.Column(db.String(100))
    
    detail =  db.Column(db.String(100))
    
    stripe_id =  db.Column(db.String(100))

    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'),
        nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    

