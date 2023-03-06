from flask import Flask, render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
# from App import db
from logging import FileHandler, WARNING


contact_blue= Blueprint("contact", __name__, static_folder="../static", template_folder="../templates")

@contact_blue.route("/contact")
def contact():
    return render_template("contact.html")

