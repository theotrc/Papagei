from flask import render_template, Blueprint, request
from flask_login import login_required, current_user
from ..models import User
from App import db


account_blue = Blueprint("account", __name__, static_folder="../static", template_folder="../templates")

@account_blue.route("/account")
@login_required
def account():

    return render_template("account.html",data={"user":current_user})


## information perso

@account_blue.route("/personalinformations")
@login_required
def personal_informations():

    return render_template("personal_informations.html",data={"user":current_user})



@account_blue.route("/personalinformationsmodify",  methods=["GET"])
@login_required
def modify():

    return render_template("personal_informationsform.html",data={"user":current_user})


@account_blue.route("/personalinformationsmodify", methods=["POST"])
@login_required
def modify_post():

    name = request.form.get("name")
    firstname = request.form.get("firstname")
    address = request.form.get("address")
    user = User.query.filter_by(id=current_user.id)
    try:
        user.update(values={"name":name, "firstname":firstname,"address":address})
        db.session.commit()
    except Exception as e:
        return render_template("personal_informations.html", data={"user":current_user})

    return render_template("personal_informations.html", data={"user":current_user})
