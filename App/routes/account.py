from flask import Flask, render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
# from App import db
from logging import FileHandler, WARNING


account_blue = Blueprint("account", __name__, static_folder="../static", template_folder="../templates")

@account_blue.route("/account")
def account():
    return render_template("account.html")

