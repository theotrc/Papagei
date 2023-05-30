from flask import redirect, Blueprint, render_template
from App import stripe
from flask import request


checkout_blue= Blueprint("checkout", __name__, static_folder="../static", template_folder="../templates")



@checkout_blue.route('/checkout')
def checkout():

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