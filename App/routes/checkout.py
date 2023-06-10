from flask import Blueprint, render_template,url_for
from App import stripe, stripe_public_key, pwd, email_sender
from flask import request
from ..models import Cart, Order, User
from flask_login import current_user
from flask_login import  login_required
from App import db
from email.message import EmailMessage
import smtplib
import ssl

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

    # paiement validé | ajout du panier dans un commande

    session_id = request.args.get('session_id')
    payment_status = stripe.checkout.Session.retrieve(session_id)["payment_status"]
    print(stripe.checkout.Session.retrieve(session_id)["customer_email"])
    if payment_status == "paid":

        cart_id = Cart.query.filter_by(user_id=current_user.id, status="N").first().id
        new_order = Order(status="paiement validé",stripe_id=session_id,cart_id= cart_id, user_id=current_user.id)
        
        Cart.query.filter_by(user_id=current_user.id, status="N").update(values={"status":"V"})
        
        db.session.add(new_order)
        db.session.commit()

        ##creation d'un nouveau panier
        cart = Cart.query.filter_by(user_id = current_user.id, status = "N").first()
        if not cart:
            new_cart = Cart(user_id = current_user.id)
            db.session.add(new_cart)
            db.session.commit()
        
        email_receiver = User.query.filter_by(id=current_user.id).first().email
        order_id = Order.query.filter_by(cart_id=cart_id, user_id=current_user.id).first().id
        subject = f"commade numéro {order_id}"
        body = f"merci pour votre commade, vous pouvez suivre son avancement dans l'onglet compte puis mes commandes"

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] =  subject
        em.set_content(body)



        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, pwd)
            smtp.sendmail(email_sender,email_receiver,em.as_string())

        return render_template("success.html")
    else: return "echec"

@checkout_blue.route('/cancel')
@login_required
def cancel():
    return render_template("cancel.html")

