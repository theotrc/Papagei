from flask import render_template, Blueprint, request
from ..models import Item, Collection
from datetime import date, datetime


home_blueprint= Blueprint("home", __name__, static_folder='../static', template_folder='../templates')


@home_blueprint.route("/home")
def home():
    item = Item.query.with_entities(Item.price, Item.image, Item.id,Item.title).order_by(Item.sort).all() 
    return render_template("accueil.html", items = item, byte = bytes())




@home_blueprint.route("/temporarycollection")
def temporary_collection():
    return render_template("temporary_collection.html")



@home_blueprint.route("/patern")
def patern():
    return render_template("patern.html")

@home_blueprint.route("/tosave")
def to_save():
    return render_template("to_save.html")

@home_blueprint.route("/oldcollection")
def old_collection():
    return render_template("old_collection.html")