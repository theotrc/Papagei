from flask import render_template,Blueprint
from ..models import Item, ItemImage

sale_blue= Blueprint("sale", __name__, static_folder='../static', template_folder='../templates')
@sale_blue.route("/sale<id>")
def sale_page(id):


    item = Item.query.filter(Item.id == int(id)).first()
    second_images = ItemImage.query.filter(ItemImage.item_id == int(id)).all()
    print(second_images)
    return render_template("page_achat.html", item = item, second_images=second_images)