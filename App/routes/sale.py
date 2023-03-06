from flask import Flask, render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
# from App import db
from flask_login import login_user, login_required, current_user, logout_user


sale_blue= Blueprint("sale", __name__, static_folder="../static", template_folder="../templates")


@sale_blue.route("/sale")
@login_required
def sale_page():
    return render_template("page_achat.html")