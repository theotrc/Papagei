from flask import redirect, Blueprint, render_template
from App import stripe
from flask import request


checkout_blue= Blueprint("checkout", __name__, static_folder="../static", template_folder="../templates")



@checkout_blue.route('/checkout')
def checkout():
    
    session = stripe.checkout.Session.create(
        payement_method_types=["card"],
        line_items=[{"price":10, "quantity":1}], 
        mode="payement", 
        success_url="https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://example.com/cancel",
    )

    return render_template("checkout.html")




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