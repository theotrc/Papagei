from flask import Flask, render_template, request, redirect, url_for, Blueprint,flash
from App import db
from logging import FileHandler, WARNING
from ..models import User, Item, Cart, Cart_item, ItemImage
from flask_login import login_user, login_required, current_user, logout_user
from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm
import os
import base64
# class UploadFileForm(FlaskForm):
#     file = FileField('File')
#     submit = SubmitField("Upload File")

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

            poids = request.form.get('poids')

            image1=request.files['image']
            image1 = image1.stream.read()
            image1 = base64.encodebytes(image1)

            titre = request.form.get('titre')
            new_item = Item(
                description = description,
                composition=composition,
                color=couleur,
                weight=poids,
                  image = image1,
                    price = float(prix), title = titre)
            db.session.add(new_item)
            db.session.commit()

            images = request.files.getlist('second_images')
            
            itemid = Item.query.all()[-1].id
            print(images)
            for image in images:
                # Vérifier si une image a été sélectionnée
                if image.filename != '':
                    print(image)
                    image = image.stream.read()
                    image = base64.encodebytes(image)
                    new_pic = ItemImage(image=image, item_id=itemid)
                    db.session.add(new_pic)
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