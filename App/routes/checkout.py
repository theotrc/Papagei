from flask import Blueprint, render_template,url_for
from App import stripe, stripe_public_key
from flask import request
from ..models import Cart, Order
from flask_login import current_user
from flask_login import  login_required
from App import db

checkout_blue= Blueprint("checkout", __name__, static_folder="../static", template_folder="../templates")



@checkout_blue.route('/checkout')
@login_required
def checkout():
    
    checkout_price = int(float(Cart.query.filter_by(user_id=current_user.id,status="N").first().price) * 100)

    
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price_data": {
        "currency": "eur",
        "unit_amount": checkout_price,
        "product_data": {
          "name": "total du panier",
        },
      },
      "quantity": 1,
    },], 
        mode="payment", 
        success_url=url_for("checkout.success",_external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for("checkout.cancel", _external=True),
    )
    print(stripe.checkout.Session.retrieve(session["id"])["status"])
    return render_template( 
                            "checkout.html",
                            checkout_session_id=session["id"],
                            checkout_public_key=stripe_public_key
                        )

@checkout_blue.route('/success')
@login_required
def success():

    # paiement validé | ajout du pannier dans un commande

    session_id = request.args.get('session_id')
    payment_status = stripe.checkout.Session.retrieve(session_id)["payment_status"]

    if payment_status == "paid":

        cart_id = Cart.query.filter_by(user_id=current_user.id, status="N").first().id
        new_order = Order(status="paiement validé",stripe_id=session_id,cart_id= cart_id, user_id=current_user.id)
        
        Cart.query.filter_by(user_id=current_user.id, status="N").update(values={"status":"V"})
        
        db.session.add(new_order)
        db.session.commit()
    return render_template("success.html")

@checkout_blue.route('/cancel')
@login_required
def cancel():
    return render_template("cancel.html")

