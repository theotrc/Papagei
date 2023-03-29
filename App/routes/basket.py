from flask import Flask, render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from App import db
from logging import FileHandler, WARNING
from flask_login import login_user, login_required, current_user, logout_user
from ..models import Item, Cart, Cart_item, User


basket_blue= Blueprint("basket", __name__, static_folder="../static", template_folder="../templates")

@basket_blue.route("/basket<id>", methods=['POST'])
@login_required
def basket_post(id):
    size = request.form.get('size')
    quantity = request.form.get('quantity')
    cart = Cart.query.filter_by(user_id = current_user.id).first()
    if not cart:
        new_cart = Cart(user_id = current_user.id)
        db.session.add(new_cart)
        db.session.commit()
        cart = Cart.query.filter_by(user_id = current_user.id).first()

    new_item = Cart_item(item_quantity=quantity, order_status="default", cart_item_id=cart.id, item_id=1)
    db.session.add(new_item)
    db.session.commit()

    items = Cart_item.query.all()

    return render_template("basket.html", items = items)

@basket_blue.route("/basket")
@login_required
def basket():
    items = Cart_item.query.all()


    return render_template("basket.html", items = items)