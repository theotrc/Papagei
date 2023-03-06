from flask import Flask, render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
# from App import db
from logging import FileHandler, WARNING


news_blue= Blueprint("news", __name__, static_folder="../static", template_folder="../templates")


@news_blue.route("/news")
def news():
    return render_template("news.html")
