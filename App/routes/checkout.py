from flask import redirect, Blueprint, render_template,url_for
from App import stripe, stripe_public_key
from flask import request
from ..models import Cart, User
from flask_login import current_user
from flask_login import  login_required

checkout_blue= Blueprint("checkout", __name__, static_folder="../static", template_folder="../templates")



@checkout_blue.route('/checkout')
@login_required
def checkout():
    
    checkout_price = int(float(Cart.query.filter_by(user_id=current_user.id).first().total_price) * 100)

    
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
    return render_template("success.html")

@checkout_blue.route('/cancel')
@login_required
def cancel():
    return render_template("cancel.html")


# @checkout_blue.route('/checkout', methods=['POST'])
# def checkout_post():
#     amount = request.form["amount"]
#     token = request.form["stripeToken"]

#     charge = stripe.Charge.create(
#     amount=amount,
#     currency='EUR',
#     source=token,
#     description='Paiement test'
#   )

#   Traitez le résultat du paiement ici et affichez une confirmation à l'utilisateur

#     return 'Paiement effectué avec succès !'