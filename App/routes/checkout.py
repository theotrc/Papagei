from flask import Blueprint, render_template,url_for
from App import stripe, stripe_public_key, pwd, email_sender
from flask import request
from ..models import Cart, Order, User, Cart_item, Item
from flask_login import current_user
from flask_login import  login_required
from App import db
from App.utils import send_mail

checkout_blue= Blueprint("checkout", __name__, static_folder="../static", template_folder="../templates")



@checkout_blue.route('/checkout')
@login_required
def checkout():
    
    checkout_price = int(float(Cart.query.filter_by(user_id=current_user.id,status="N").first().price) * 100)

    cart = Cart.query.filter_by(user_id=current_user.id,status="N").first()
    if cart.cart_weight < 250 :
        checkout_price = checkout_price + 495

    elif cart.cart_weight < 500 and cart.cart_weight >= 250:
        checkout_price = checkout_price + 670
    elif cart.cart_weight < 750 and cart.cart_weight >= 500:
        checkout_price = checkout_price + 760

    elif cart.cart_weight < 1000 and cart.cart_weight >= 750:
        checkout_price = checkout_price + 825

    elif cart.cart_weight < 2000 and cart.cart_weight >= 1000:
        checkout_price = checkout_price + 955

    elif cart.cart_weight >= 2000:
        checkout_price = checkout_price + 1465

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


        for item in Cart_item.query.filter_by(cart_item_id=cart_id).all():
            itemid = item.item_id
            quantity = item.item_quantity
            item_quantity = Item.query.filter_by(id=itemid).first().quantity

            new_quantity = int(item_quantity) - int(quantity)
            Item.query.filter_by(id=itemid).update(values={"quantity":new_quantity})
            db.session.commit()



        new_order = Order(status="Paiement validé",stripe_id=session_id,cart_id= cart_id, user_id=current_user.id)
        
        Cart.query.filter_by(user_id=current_user.id, status="N").update(values={"status":"V"})
        
        db.session.add(new_order)
        db.session.commit()

        ##creation d'un nouveau panier
        cart = Cart.query.filter_by(user_id = current_user.id, status = "N").first()
        if not cart:
            new_cart = Cart(user_id = current_user.id)
            db.session.add(new_cart)
            db.session.commit()
        try:
            cart = Cart.query.filter_by(user_id = current_user.id, status = "N").first()
            email_receiver = User.query.filter_by(id=current_user.id).first().email
            order_id = Order.query.filter_by(cart_id=cart_id, user_id=current_user.id).first().id
            subject = f"papagei - Commande Numéro {order_id} confirmée"
            body = f"Bonjour {str(cart.user.firstname).capitalize()}, \n Merci pour votre commande (N.{order_id}), elle est bien enregistrée et sera traitée au plus vite.\n\nLes articles sont faits main et à la demande, il faut compter au maximum deux semaines pour le délai de fabrication.Vous pouvez suivre son avancement sur notre site internet dans l'onglet 'Compte' puis 'Mes commandes'.\n\nUn mail vous sera communiqué lors de l'expédition de votre commande.\n\nÀ très vite sur www.papagei-shop.fr.\nL'équipe papagei"
            send_mail(body=body,subject=subject, user_mail=email_receiver)
        except Exception as e:
            return render_template("success.html")


        return render_template("success.html")
    else: return "echec"

@checkout_blue.route('/cancel')
@login_required
def cancel():
    return render_template("cancel.html")

