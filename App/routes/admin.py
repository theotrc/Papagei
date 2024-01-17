from flask import render_template, request, redirect, url_for, Blueprint,flash
from sqlalchemy import values
from App import db
from ..models import Cart, Item, ItemImage, Order, Item_size, Cart_item,Collection, ItemColor
from flask_login import login_required, current_user
import base64


import os
from App.utils import send_mail




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
        
        ##modifier les prix des pannier
        del_item = Item.query.filter_by(id=int(id)).first()
        del_cart_item = Cart_item.query.filter_by(item_id=int(id)).all()
        for cart_item in del_cart_item:
            
            current_cart=cart_item.cart
            cart_price = current_cart.price
            cart_weight = current_cart.cart_weight
            item_quantity = cart_item.item_quantity
            item_price = del_item.price
            item_weight = del_item.weight
            
            
            new_weight = cart_weight - (item_weight * item_quantity)
            new_price = cart_price - (item_price * item_quantity)
            Cart.query.filter_by(id=current_cart.id).update(values = {"cart_weight":new_weight,"price":new_price})
            db.session.commit()
            
            
            
            db.session.delete(cart_item)
        

        del_sizes = Item_size.query.filter_by(item_id=int(id)).all()
        for size in del_sizes:
            db.session.delete(size)
            
        del_colors = ItemColor.query.filter_by(item_id=int(id)).all()
        for color in del_colors:
            db.session.delete(color)
        

        del_images = ItemImage.query.filter_by(item_id=int(id)).all()
        for image in del_images:
            db.session.delete(image)
        
        
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

            about_model = request.form.get("about_model")
            poids = request.form.get('poids')
            image1=request.files['image']
            image1 = image1.stream.read()
            image1 = base64.encodebytes(image1)

            titre = request.form.get('titre')
            new_item = Item(
                description = description,
                composition=composition,
                weight=float(poids),
                  image = image1,
                    price = float(prix),
                    title = titre,
                    about_model=about_model)
            db.session.add(new_item)
            db.session.commit()

            images = request.files.getlist('second_images')
            sizes = request.form.getlist('size')
            itemid = Item.query.filter_by(description=description, composition=composition,title=titre,weight=float(poids),price = float(prix), image=image1).first().id
            colors = request.form.getlist('colors')
            quantities = request.form.getlist("quantity")
            
            
            data = list(zip(colors, quantities))
            colors_and_quantities = dict(data)
            
            print(colors_and_quantities)
            # ajout des images en bdd
            for image in images:
                # Vérifier si une image a été sélectionnée
                if image.filename != '':

                    image = image.stream.read()
                    image = base64.encodebytes(image)
                    new_pic = ItemImage(image=image, item_id=itemid)
                    db.session.add(new_pic)
                    db.session.commit()

            # ajout des tailles en bdd
            for size in sizes:
                size = size.upper()
                print(size)
                new_size = Item_size(size=size, item_id=itemid)
                db.session.add(new_size)
                db.session.commit()
                
            # ajout des couleurs en bdd
            for color in colors_and_quantities.keys():
                quantity = int(colors_and_quantities[color])
                color = color.upper()
                new_color = ItemColor(name=color,quantity=quantity, item_id=itemid)
                db.session.add(new_color)
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
                    body = f"Bonjour {str(firstname).capitalize()},\nVotre commande N. {id} est en cours de confection,un mail vous sera envoyé au moment de son expédition. Vous pouvez à tout moment voir son avancement sur www.papagei-shop.fr dans la rubrique 'Compte' puis 'Mes commandes'.\nÀ très vite,\nL'équipe papagei."

                elif status.lower()=="expédiée":
                    subject = f"papagei - Commande N. {id} - {status}"
                    body = f"Bonjour {str(firstname).capitalize()},\nVotre commande N. {id} est expédiée, vous recevrez des notififications concernant la livraison de votre colis par La Poste à l'adresse mail utilisée pour la commande.\nÀ très vite,\nL'équipe papagei."

                elif status.lower()=="annulée":
                    subject = f"papagei - Commande N. {id} - {status}"
                    body = f"Bonjour {str(firstname).capitalize()},\nVotre commande N. {id} a été annulée. N'hésitez pas à contacter le service client à cette adresse mail: contact.papageishop@gmail.com.\nÀ très vite,\nL'équipe papagei."


                send_mail(body=body,subject=subject, user_mail=email_receiver)

            return redirect(url_for("admin.admincmd"))
        except Exception as e:
            return redirect(url_for("admin.admincmd"))
    else: return redirect(url_for("home.home"))



@admin.route("/modfifyitem<id>")
@login_required
def modify_item(id):
    if current_user.is_admin:
        item = Item.query.filter_by(id=int(id)).first()
        collections = Collection.query.all()
        return render_template("modifyitem.html", item=item, collections=collections)
    else:redirect(url_for("home.home"))





@admin.route("/modfifyitem<id>", methods=["POST"])
@login_required
def modify_item_post(id):
    if current_user.is_admin:
        
        
        
        sizes = request.form.getlist('sizes')
        colors = request.form.getlist('colors')
        current_colors= request.form.getlist("currentColors")
        current_colors_old_name = request.form.getlist("currentColorsOldNames")
        current_quantities = request.form.getlist("currentQuantities")
        
        current_size = request.form.getlist("current_sizes")
        current_size_old_name = request.form.getlist("current_sizes_old_name")
        quantities = request.form.getlist("quantity")
        
        data = list(zip(colors, quantities))
        colors_and_quantities = dict(data)
        
        data = list(zip(current_colors_old_name, current_quantities))
        current_colors_and_quantities = dict(data)
        
        data = list(zip(current_colors_old_name, current_colors))
        current_colors_names_old_names = dict(data)
        
        data = list(zip(current_size_old_name, current_size))
        current_sizes_names = dict(data)
        
        item = Item.query.filter_by(id=int(id))
        item_color = ItemColor.query.filter_by(item_id=int(id))
        
        item_sizes = Item_size.query.filter_by(item_id=int(id))
        
        
        ### AJOUT / MODIFICATION / SUPRESSION
        
        # mise à jour des tailles déjà existantes
        for current_size in current_sizes_names.keys():
            new_size_name = str(current_sizes_names[current_size]).upper()
            size_name = str(current_size).upper()
            delete_item_size = request.form.get(f"delete_size_{current_size}")
            if delete_item_size:
                delete_item_size = item_sizes.filter_by(size=size_name).first()
                db.session.delete(delete_item_size)
            else:
            
                if size_name == new_size_name:
                    continue
                else:
                    item_sizes.filter_by(size=size_name).update(values={"size":new_size_name})
                
        db.session.commit()
        
        for size in sizes:
            new_size = str(size).upper()
            new_size_item = Item_size(size=new_size, item_id=int(id))
            db.session.add(new_size_item)
        db.session.commit()
        
        # mise à jour des couleurs déjà existantes
        for current_color in current_colors_and_quantities.keys():
            delete_item_color = request.form.get(f"delete_color_{current_color}")
            if delete_item_color:
                delete_item_color = item_color.filter_by(name=current_color).first()
                db.session.delete(delete_item_color)
            else:
                new_quantity = current_colors_and_quantities[current_color]
                new_name = str(current_colors_names_old_names[current_color]).upper()
                item_color.filter_by(name=current_color).update(values={"quantity":int(new_quantity),"name":new_name})
                
            
        
        db.session.commit()
            
        # for color in item.first().colors:
        #     color_id= color.id
        #     html_name = f"quantity_{color_id}"
        #     quantity = request.form.get(html_name)
        #     ItemColor.query.filter_by(id=int(color_id)).update(values={"quantity": int(quantity)})
            
        # ajout des couleurs en bdd
        for color in colors_and_quantities.keys():
            quantity = int(colors_and_quantities[color])
            color = color.upper()
            new_color = ItemColor(name=color,quantity=quantity, item_id=int(id))
            db.session.add(new_color) 
        
        
        
        sort = int(request.form.get("sort"))
        item.update(values={"sort":sort})
        db.session.commit()
        
        
        return redirect(url_for("admin.adminitems"))
    else:redirect(url_for("home.home"))
    