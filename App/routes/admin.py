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

        return render_template("admin.html",data={"user":current_user})
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
            
            image2=request.files['image2']
            image2 = image2.stream.read()
            image2 = base64.encodebytes(image2)

            image3=request.files['image3']
            image3 = image3.stream.read()
            image3 = base64.encodebytes(image3)

            image4=request.files['image4']
            image4 = image4.stream.read()
            image4 = base64.encodebytes(image4)

            image5=request.files['image5']
            image5 = image5.stream.read()
            image5 = base64.encodebytes(image5)

            image6=request.files['image6']
            image6 = image6.stream.read()
            image6 = base64.encodebytes(image6)
            
            image7=request.files['image7']
            image7 = image7.stream.read()
            image7 = base64.encodebytes(image7)

            image8=request.files['image8']
            image8 = image8.stream.read()
            image8 = base64.encodebytes(image8)

            image9=request.files['image9']
            image9 = image9.stream.read()
            image9 = base64.encodebytes(image9)

            image10=request.files['image10']
            image10 = image10.stream.read()
            image10 = base64.encodebytes(image10)

            image11=request.files['image11']
            image11 = image11.stream.read()
            image11 = base64.encodebytes(image11)

            



            titre = request.form.get('titre')
            new_item = Item(
                description = description,
                composition=composition,
                color=couleur,
                weight=poids,
                  main_image = image1, image2=image2,image3=image3,image4=image4,image5=image5,image6=image6,image7=image7,image8=image8,image9=image9,image10=image10,image11=image11,
                    price = float(prix), title = titre)
            db.session.add(new_item)
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
@admin.route("/admin_page/remove")
@login_required
def remove_item():
    if current_user.is_admin:
        return "ok"
    else:
        return "no"


@admin.route("/admin_pagetest", methods=['POST'])
@login_required
def add_item_posttest():
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