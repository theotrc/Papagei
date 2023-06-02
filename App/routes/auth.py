from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from App import db
from App.utils import generate_code
from ..models import User
from logging import FileHandler, WARNING
from flask_login import login_user, login_required, current_user, logout_user
from datetime import date, datetime, timedelta
from hashlib import sha256

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
    if not password or len(password)<8:
        flash("le mot de passe doit faire 8 caractères minimum", "info")
        return render_template('signup.html')

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


    return render_template('Password.html')

@auth_blue.route("/resetpwd", methods=['POST'])
def resetpwd_post():

    email_receiver = request.form.get('email')

    
    user = User.query.filter_by(email=email_receiver).first()

    ## if user exist
    if user:
        id = user.id

        code = sha256(str(generate_code()).encode()).hexdigest()
        expiry = datetime.now() + timedelta(days=1)


        User.query.filter_by(id=id).update(values={"reset_token":code,"reset_token_expiry":expiry})
        db.session.commit()


        subject = "réinitialisation de mot de passe"
        body = f"lien de réinitialisation: http://10.25.1.37:8000/mailvalidation/{id}/{code}"

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] =  subject
        em.set_content(body)



        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, pwd)
            smtp.sendmail(email_sender,email_receiver,em.as_string())

        message = f"Un email vous a été envoyé"
        flash(message, "info")

    elif not user:

        message = f"L'adresse mail que vous avez rentré n'est associé à aucun compte"
        flash(message, "info")

    return render_template("Password.html")

@auth_blue.route("/mailvalidation/<id>/<code>")
def mailvalidation(id,code):
    
    user = User.query.filter_by(id=int(id)).filter_by(reset_token=code).first()
    if user:
        if user.reset_token_expiry > datetime.now():
            return render_template('ValidateMail.html', id=id,code=code)
        else:
            return "False"
    else:
        return "False"



@auth_blue.route('/mailvalidation/<id>/<code>', methods=['POST'])
def change_pwd(id, code):
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password == confirm_password:    
        try:



            User.query.filter_by(id=int(id)).filter_by(reset_token=code).update(values={"reset_token":None,
                                                                                "reset_token_expiry":None,
                                                                                "password":generate_password_hash(password, method='sha256')})
            db.session.commit()
        except Exception as e:
            return "error"
    else:
        flash("les deux mots de passe ne sont pas indentiques", "info")
        return render_template('ValidateMail.html', id=id,code=code)
    
    return redirect(url_for('auth.login'))
