from flask import Flask, render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
# from App import db
from logging import FileHandler, WARNING
from ..models import User
from flask_login import login_user, login_required, current_user, logout_user


admin = Blueprint("admin", __name__, static_folder="../static", template_folder="../templates")

@admin.route("/admin_page")
@login_required
def add_item():
    if current_user.is_admin:
        return render_template("admin.html",data={"user":current_user})
    else: return url_for("home.home")