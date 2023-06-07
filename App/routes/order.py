from flask import render_template, Blueprint
from ..models import Order
from flask_login import login_required, current_user


order_blue= Blueprint("order", __name__, static_folder='../static', template_folder='../templates')


@order_blue.route("/orders")
@login_required
def orders():

    orders = Order.query.filter_by(user_id=current_user.id).all()
    
    return render_template("orders.html", orders = orders)