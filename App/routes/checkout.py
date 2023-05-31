from flask import redirect, Blueprint, render_template,url_for
from App import stripe, stripe_public_key
from flask import request


checkout_blue= Blueprint("checkout", __name__, static_folder="../static", template_folder="../templates")



@checkout_blue.route('/checkout')
def checkout():
    
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price_data": {
        "currency": "usd",
        "unit_amount": 500,
        "product_data": {
          "name": "name of the product",
        },
      },
      "quantity": 1,
    },], 
        mode="payment", 
        success_url=url_for("home.home",_external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for("basket.basket", _external=True),
    )

    return render_template(
                            "checkout.html",
                            checkout_session_id=session["id"],
                            checkout_public_key=stripe_public_key
                        )




@checkout_blue.route('/checkout', methods=['POST'])
def checkout_post():
    amount = request.form["amount"]
    token = request.form["stripeToken"]

    charge = stripe.Charge.create(
    amount=amount,
    currency='EUR',
    source=token,
    description='Paiement test'
  )

  # Traitez le résultat du paiement ici et affichez une confirmation à l'utilisateur

    return 'Paiement effectué avec succès !'