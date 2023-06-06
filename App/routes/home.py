from flask import render_template, Blueprint
from ..models import Item


home_blueprint= Blueprint("home", __name__, static_folder='../static', template_folder='../templates')


@home_blueprint.route("/home")
def home():

    item = Item.query.all()  
    
    return render_template("accueil.html", items = item, byte = bytes())
