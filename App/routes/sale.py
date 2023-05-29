from flask import render_template,Blueprint
from ..models import Item

sale_blue= Blueprint("sale", __name__, static_folder='../static', template_folder='templates')
@sale_blue.route("/sale<id>")
def sale_page(id):


    item = Item.query.filter(Item.id == int(id)).first()
    return render_template("page_achat.html", item = item)