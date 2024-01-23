from flask import render_template,Blueprint
from ..models import Item, Item_size, ItemColor, ItemImage

sale_blue= Blueprint("sale", __name__, static_folder='../static', template_folder='../templates')
@sale_blue.route("/sale<id>")
def sale_page(id):


    item = Item.query.with_entities(
        Item.id,
        Item.title,
        Item.description,
        Item.composition,
        Item.image,
        Item.price,
        Item.about_model,
        ).filter(Item.id == int(id)).first()
    # second_images = item.images

    sizes = Item_size.query.filter_by(item_id=int(id)).all()
    colors = ItemColor.query.filter_by(item_id=int(id)).all()
    second_images = ItemImage.query.filter(ItemImage.item_id == int(id)).all()
    return render_template("page_achat.html", item = item, second_images=second_images, sizes=sizes, colors = colors)