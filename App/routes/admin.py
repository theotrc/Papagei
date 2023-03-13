from flask import Flask, render_template, request, redirect, url_for, Blueprint
from App import db
from logging import FileHandler, WARNING
from ..models import User, Item, Purchased_item
from flask_login import login_user, login_required, current_user, logout_user
from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm
import os

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
    else: return url_for("home.home")

@admin.route("/admin_page", methods=['POST'])
@login_required
def add_item_post():
    if current_user.is_admin:
        description = request.form.get('description')
        prix = request.form.get('prix')
        category = request.form.get('category')
        image2=request.files['image']
        image2 = image2.stream.read()
        titre = request.form.get('titre')
        new_item = Item(description = description, image = image2, price = float(prix), category = category, title = titre)
        db.session.add(new_item)
        db.session.commit()
        return url_for("home.home")
    else: return url_for("home.home")


