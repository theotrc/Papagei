from flask import render_template, request, redirect, url_for, Blueprint,flash
from App import db
from ..models import Item, ItemImage, Order, Item_size, Cart_item
from flask_login import login_required, current_user
import base64

from email.message import EmailMessage
import smtplib
import ssl
import os


pwd =os.environ.get('MAIL_MDP')
email_sender = os.environ.get('MAIL_SENDER')
em = EmailMessage()

admin = Blueprint("admin", __name__, static_folder="../static", template_folder="../templates")





@admin.route("/adminitems")
@login_required
def adminitems():
    if current_user.is_admin:
        item = Item.query.all()  
        print(item)
        return render_template("admin_items.html",data={"user":current_user}, items=item)
    else: return redirect(url_for("home.home"))



@admin.route("/admin_page")
@login_required
def add_item():
    if current_user.is_admin:

        return render_template("admin_new_item.html",data={"user":current_user})
    else: return redirect(url_for("home.home"))



@admin.route("/adminremoveitem<id>")
@login_required
def remove_item(id):
    if current_user.is_admin:
        del_cart_item = Cart_item.query.filter_by(item_id=int(id)).all()
        for cart_item in del_cart_item:
            db.session.delete(cart_item)
        

        del_sizes = Item_size.query.filter_by(item_id=int(id)).all()
        for size in del_sizes:
            db.session.delete(size)
        

        del_images = ItemImage.query.filter_by(item_id=int(id)).all()
        for image in del_images:
            db.session.delete(image)
        del_item = Item.query.filter_by(id=int(id)).first()
        db.session.delete(del_item)
        db.session.commit()

        return redirect(url_for("admin.adminitems"))
    
    else: return redirect(url_for("home.home"))

@admin.route("/adminremoveimage<id>")
@login_required
def remove_image(id):
    if current_user.is_admin:
        del_image = ItemImage.query.filter_by(id=int(id)).first()
        db.session.delete(del_image)
        db.session.commit()

        return redirect(url_for("admin.adminitems"))
    
    else: return redirect(url_for("home.home"))


@admin.route("/admin_page", methods=['POST'])
@login_required
def add_item_post():
    if current_user.is_admin:
        try:
            ## ajout de l'article dans la bdd
            description = request.form.get('description')
            prix = request.form.get('prix')
            composition = request.form.get('composition')

            couleur = request.form.get('couleur')
            about_model = request.form.get("about_model")
            poids = request.form.get('poids')
            quantity = request.form.get('quantity')
            image1=request.files['image']
            image1 = image1.stream.read()
            image1 = base64.encodebytes(image1)

            titre = request.form.get('titre')
            new_item = Item(
                description = description,
                composition=composition,
                color=couleur,
                weight=float(poids),
                  image = image1,
                    price = float(prix),
                    title = titre,
                    quantity=int(quantity),
                    about_model=about_model)
            db.session.add(new_item)
            db.session.commit()

            images = request.files.getlist('second_images')
            sizes = request.form.getlist('size')
            itemid = Item.query.filter_by(description=description, composition=composition,title=titre,weight=float(poids),price = float(prix), image=image1).first().id

            for image in images:
                # Vérifier si une image a été sélectionnée
                if image.filename != '':

                    image = image.stream.read()
                    image = base64.encodebytes(image)
                    new_pic = ItemImage(image=image, item_id=itemid)
                    db.session.add(new_pic)
                    db.session.commit()

            for size in sizes:
                size = size.upper()
                new_size = Item_size(size=size, item_id=itemid)
                db.session.add(new_size)
                db.session.commit()

            
            message = f"article ajouté"
            flash(message, "info")
        except Exception as e:
            ## récupération de l'erreur de l'ajout + message flash
            print(e)
            message = f"erreur lors de l'ajout de l'article"
            flash(message, "info")
        return redirect(url_for("admin.add_item"))
    else: return redirect(url_for("home.home"))


@admin.route("/admin_cmd")
@login_required
def admincmd():

    if current_user.is_admin:
        orders = Order.query.all()
        return render_template("admincmd.html", orders=orders)
    else: return redirect(url_for("home.home"))

@admin.route("/cmddetails<id>")
@login_required
def details(id):

    if current_user.is_admin:
        order = Order.query.filter_by(id=int(id)).first()
        return render_template("admincmd_details.html", order=order)
    else: return redirect(url_for("home.home"))


@admin.route("/newstatus<id>", methods=["POST"])
@login_required
def newstatus(id):

    if current_user.is_admin:
        try:
            status = request.form.get("order_status")
            Order.query.filter_by(id=int(id)).update(values = {"status":status})
            db.session.commit()

            email_receiver = Order.query.filter_by(id=int(id)).first().user.email
            firstname = Order.query.filter_by(id=int(id)).first().user.firstname
            

            if status.lower() in ["en cours","expédiée", "annulée"]:

                if status.lower()=="en cours":

                    subject = f"papagei - Commande N. {id} - {status}"
                    body = f"Bonjour {firstname},\nVotre commade N. {id} est en cours de confection,un mail vous sera envoyé au moment de son expédition. Vous pouvez à tout moment voir son avancement sur www.papagei-shop.fr dans la rubrique 'Compte' puis 'Mes commandes'.\nÀ très vite,\nL'équipe papagei."

                elif status.lower()=="expédiée":
                    subject = f"papagei - Commande N. {id} - {status}"
                    body = f"Bonjour {firstname},\nVotre commade N. {id} est expédiée, vous recevrez des notififications concernant la livraison de votre colis par La Poste à l'adresse mail utilisée pour la commande.\nÀ très vite,\nL'équipe papagei."

                elif status.lower()=="annulée":
                    subject = f"papagei - Commande N. {id} - {status}"
                    body = f"Bonjour {firstname},\nVotre commande N. {id} a été annulée. N'hésitez pas à contacter le service client à cette adresse mail: contact.papageishop@gmail.com.\nÀ très vite,\nL'équipe papagei."


                em['From'] = email_sender
                em['To'] = email_receiver
                em['Subject'] =  subject
                em.set_content(body)



                context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, pwd)
                    smtp.sendmail(email_sender,email_receiver,em.as_string())


            return redirect(url_for("admin.admincmd"))
        except Exception as e:
            return redirect(url_for("admin.admincmd"))
    else: return redirect(url_for("home.home"))



@admin.route("/modfifyitem<id>")
@login_required
def modify_item(id):
    if current_user.is_admin:
        item = Item.query.filter_by(id=int(id)).first()
        return render_template("modifyitem.html", item=item)
    else:redirect(url_for("home.home"))





@admin.route("/modfifyitem<id>", methods=["POST"])
@login_required
def modify_item_post(id):
    if current_user.is_admin:
        quantity = int(request.form.get("quantity"))
        Item.query.filter_by(id=int(id)).update(values={"quantity":quantity})
        db.session.commit()
        return redirect(url_for("admin.adminitems"))
    else:redirect(url_for("home.home"))