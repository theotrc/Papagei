from flask import Flask, render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
# from App import db
from logging import FileHandler, WARNING
from flask_login import login_user, login_required, current_user, logout_user


basket_blue= Blueprint("basket", __name__, static_folder="../static", template_folder="../templates")

@basket_blue.route("/basket")
@login_required
def basket():
    return render_template("basket.html")