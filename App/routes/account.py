from flask import render_template, Blueprint, request, redirect, url_for
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
    street = request.form.get("street")
    streetnumber = request.form.get("streetnumber")
    zipcode = request.form.get("zipcode")
    city = request.form.get("city")
    country = request.form.get("country")
    addressmore = request.form.get("addressmore")

    if not addressmore:
        addressmore=""
    user = User.query.filter_by(id=current_user.id)
    try:
        user.update(values={"name":name, "firstname":firstname,"country":country,"city":city, "zipecode":zipcode, "streetnumber":streetnumber, "street":street, "addressmore":addressmore})
        db.session.commit()
    except Exception as e:
        return render_template("personal_informations.html", data={"user":current_user})

    return render_template("personal_informations.html", data={"user":current_user})



@account_blue.route("/deleteaccount", methods=["GET"])
@login_required
def deleteaccount():
    try:
        removeuser = User.query.filter_by(email=current_user.email).first()
        db.session.delete(removeuser)
        db.session.commit()
    except Exception as e:
        return redirect(url_for("account.account"))
    return redirect(url_for("home.home"))

