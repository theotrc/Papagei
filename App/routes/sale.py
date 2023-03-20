from flask import Flask, render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
# from App import db
from flask_login import login_user, login_required, current_user, logout_user
from ..models import Item


sale_blue= Blueprint("sale", __name__, static_folder="../static", template_folder="../templates")

#url sale + get image id
@sale_blue.route("/sale/<id>")
@login_required
def sale_page(id):


    item = Item.query.filter(Item.id == int(id)).first()
    return render_template("page_achat.html", item = item)