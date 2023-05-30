from flask import render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import redirect
from App import db
from flask_login import login_required, current_user
from ..models import Item, Cart, Cart_item



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
    
    basket_cost = Cart.query.filter_by(user_id=current_user.id).first().total_price
    basket_cost += float(Item.query.filter_by(id=int(id)).first().price)
    Cart.query.filter_by(user_id=current_user.id).update(values={"total_price":basket_cost})
    new_item = Cart_item(item_quantity=quantity, order_status="default", cart_item_id=cart.id, item_id=id, size=size)
    db.session.add(new_item)
    db.session.commit()


    ## get user carts
    

    return redirect(url_for("basket.basket"))

@basket_blue.route("/basket")
@login_required
def basket():
    carts = Cart.query.filter_by(user_id=current_user.id)

    return render_template("basket.html", carts = carts)


@basket_blue.route("/removeitem<id>")
@login_required
def deleteitem_basket(id):

    item = Cart_item.query.filter_by(id=int(id)).first()

    basket_cost = Cart.query.filter_by(user_id=current_user.id).first().total_price
    basket_cost += - float(Item.query.filter_by(id=item.item_id).first().price)

    Cart.query.filter_by(user_id=current_user.id).update(values={"total_price":basket_cost})
    
    db.session.delete(item)
    db.session.commit()


    return redirect(url_for("basket.basket"))


