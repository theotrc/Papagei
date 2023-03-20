from flask import Flask, render_template, request, redirect, url_for, Blueprint,flash
from App import db
from logging import FileHandler, WARNING
from ..models import User, Item, Purchased_item
from flask_login import login_user, login_required, current_user, logout_user
from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm
import os
import base64
# class UploadFileForm(FlaskForm):
#     file = FileField('File')
#     submit = SubmitField("Upload File")

admin = Blueprint("admin", __name__, static_folder="../static", template_folder="../templates")

@admin.route("/admin_page")
@login_required
def add_item():
    if current_user.is_admin:
        # form = UploadFileForm()
        # if form.validate_on_submit():
        #     print('hiuorehziofjhiozejfiofjjjjjjjjjjjjjjjjjjjjjjjjjj')
        #     file = form.file.data
        #     file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),'static/files',secure_filename(file.file_name)))
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
            category = request.form.get('category')
            image2=request.files['image']
            image2 = image2.stream.read()
            image2 = base64.encodebytes(image2)
            titre = request.form.get('titre')
            new_item = Item(description = description, image = image2, price = float(prix), category = category, title = titre)
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


