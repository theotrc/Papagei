from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from App import db
from ..models import User
from logging import FileHandler, WARNING
from flask_login import login_user, login_required, current_user, logout_user

import smtplib
from email.message import EmailMessage
import ssl
import os


pwd =os.environ.get('EMAIL_PWD')
email_sender = os.environ.get('EMAIL_SENDER')
email_receiver = 'theotricot12@gmail.com'



auth_blue= Blueprint("auth", __name__, static_folder="../static", template_folder="../templates")

#routes for login
@auth_blue.route('/signup')
def signup():
    return render_template('signup.html')


@auth_blue.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    firstname = request.form.get('firstname')
    adress = request.form.get('adress')
    country = request.form.get('country')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'),firstname = firstname, address=adress,country=country, is_admin=False)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth_blue.route('/login')
def login():
    return render_template('login.html')


@auth_blue.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    

    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        message = f"Utilisateur ou mot de passe incorrect"
        flash(message, "info")
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('home.home'))

@auth_blue.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))



@auth_blue.route('/resetpwd')
def resetpwd():
    subject = "réinitialisation de mot de passe"
    body = """
    rest password
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] =  subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, pwd)
        smtp.sendmail(email_sender,email_receiver,em.as_string())

    return "un mail vous a été envoyé"


