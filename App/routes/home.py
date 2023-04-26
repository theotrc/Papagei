from flask import Flask, render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
# from App import db
# from logging import FileHandler, WARNING
from ..models import Item
import base64


home_blueprint= Blueprint("home", __name__, static_folder='../static', template_folder='templates')


@home_blueprint.route("/home")
def home():

    item = Item.query.all()  
    
    return render_template("accueil.html", item = item)
