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
    color=request.form.get("color")
    cart = Cart.query.filter_by(user_id = current_user.id, status = "N").first()
    if not cart:
        new_cart = Cart(user_id = current_user.id)
        db.session.add(new_cart)
        db.session.commit()
        cart = Cart.query.filter_by(user_id = current_user.id, status = "N" ).first()
    
    basket_cost = Cart.query.filter_by(user_id=current_user.id, status="N").first().price
    basket_cost += float(Item.query.filter_by(id=int(id)).first().price) *int(quantity)

    basket_weight = Cart.query.filter_by(user_id=current_user.id, status="N").first().cart_weight
    basket_weight += float(Item.query.filter_by(id=int(id)).first().weight) *int(quantity)


    Cart.query.filter_by(user_id=current_user.id, status = "N").update(values={"price":basket_cost, "cart_weight": basket_weight})


    new_item = Cart_item(item_quantity=quantity, cart_item_id=cart.id, item_id=int(id),color=color, size=size)
    db.session.add(new_item)
    db.session.commit()


    ## get user carts
    

    return redirect(url_for("basket.basket"))

@basket_blue.route("/basket")
@login_required
def basket():
    carts = Cart.query.filter_by(user_id=current_user.id, status="N")

    if carts.first().cart_weight < 250 :
        delivery_price = 4.95

    elif carts.first().cart_weight < 500 and carts.first().cart_weight >= 250:
        delivery_price = 6.70
    elif carts.first().cart_weight < 750 and carts.first().cart_weight >= 500:
        delivery_price =  + 7.60

    elif carts.first().cart_weight < 1000 and carts.first().cart_weight >= 750:
        delivery_price =  + 8.25

    elif carts.first().cart_weight < 2000 and carts.first().cart_weight >= 1000:
        delivery_price =  + 9.55

    elif carts.first().cart_weight >= 2000:
        delivery_price =  14.65

    return render_template("basket.html", carts = carts, delivery_price=delivery_price)


@basket_blue.route("/removeitem<id>")
@login_required
def deleteitem_basket(id):

    item = Cart_item.query.filter_by(id=int(id)).first()

    basket_cost = Cart.query.filter_by(user_id=current_user.id, status="N").first().price
    basket_cost += - float(Item.query.filter_by(id=item.item_id).first().price)*int(item.item_quantity)

    basket_weight = Cart.query.filter_by(user_id=current_user.id, status="N").first().cart_weight
    basket_weight += - float(Item.query.filter_by(id=item.item_id).first().weight)*int(item.item_quantity)

    Cart.query.filter_by(user_id=current_user.id, status="N").update(values={"price":basket_cost, "cart_weight":basket_weight})
    
    db.session.delete(item)
    db.session.commit()


    return redirect(url_for("basket.basket"))


