from flask import render_template, request, redirect, url_for, Blueprint, flash
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from App import db,pwd, email_sender
from App.utils import generate_code
from ..models import User
from flask_login import login_user, login_required, logout_user
from datetime import datetime, timedelta
from hashlib import sha256
import os
site_address = os.environ.get("SITE_ADDRESS")

from App.utils import send_mail




auth_blue= Blueprint("auth", __name__, static_folder="../static", template_folder="../templates")

#routes for login
@auth_blue.route('/signup')
def signup():
    return render_template('signup.html')


@auth_blue.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    email = email.lower()
    name = request.form.get('name').lower()
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    firstname = request.form.get('firstname').lower()
    addressmore = request.form.get("addressmore")
    phone = request.form.get("phone")

    city = request.form.get('city').lower()
    zipcode = int(request.form.get('zipcode'))
    street = request.form.get('street').lower()
    street_number = request.form.get('street_number')

    country = request.form.get('country')

    if not addressmore:
        addressmore=""

    user = User.query.filter_by(email=email).first()
    
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))
    if not password or len(password)<8:
        flash("le mot de passe doit faire 8 caractères minimum", "info")
        return render_template('signup.html')
    if password == confirm_password: 
        try:
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_user = User(
                            email=email,
                            name=name,
                            password=generate_password_hash(password, method='sha256'),
                            firstname = firstname,
                            street= street,
                            city=city,
                            zipecode=zipcode,
                            streetnumber=street_number,
                            country=country,
                            addressmore=addressmore,
                            phone=phone,
                            is_admin=False
                                )

            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            user = User.query.filter_by(email=email).first()
            
            
            id = user.id

            code = sha256(str(generate_code()).encode()).hexdigest()
            expiry = datetime.now() + timedelta(days=1)


            User.query.filter_by(id=id).update(values={"reset_token":code,"reset_token_expiry":expiry})
            db.session.commit()


            subject = "papagei - Validation de compte"
            body = f"Bienvenue {str(firstname).capitalize()},\nCliquez ici pour valider la création de votre compte: {site_address}accountvalidation{id}?code={code}"

            send_mail(body=body,subject=subject, user_mail=email)

        


            return render_template("account_validation.html")
        except Exception as e:
            print(e)
            flash("Une erreur s'est produite lors de la création de votre compte", "info")
            return render_template('signup.html')
    else:
        flash("les deux mots de passe ne sont pas indentiques", "info")
        return render_template('signup.html')

@auth_blue.route('/login')
def login():
    return render_template('login.html')


@auth_blue.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    email=email.lower()
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
    if user.verify_account:
        login_user(user, remember=remember)
        return redirect(url_for('home.home'))
    else: return redirect(url_for('auth.login'))


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
        firstname=user.firstname

        subject = "papagei - Réinitialisation de mot de passe"
        body = f"Bonjour {str(firstname).capitalize()},\n Pour réinitialiser votre Mot de Passe veuillez cliquer sur ce lien: {site_address}mailvalidation{id}?code={code} \n\nÀ très vite sur papagei-shop.fr"

        send_mail(body=body,subject=subject, user_mail=email_receiver)

        message = f"Un email vous a été envoyé"
        flash(message, "info")

    elif not user:

        message = f"L'adresse mail que vous avez rentré n'est associée à aucun compte"
        flash(message, "info")

    return render_template("Password.html")

@auth_blue.route("/mailvalidation<id>")
def mailvalidation(id):
        
    code = request.args.get("code")
    print(code)
    user = User.query.filter_by(id=int(id)).filter_by(reset_token=code).first()
    if user:
        if user.reset_token_expiry > datetime.now():
            return render_template('ValidateMail.html', id=id,code=code)
        else:
            return "False"
    else:
        return "False"



@auth_blue.route('/mailvalidation<id>', methods=['POST'])
def change_pwd(id):
    code = request.args.get("code")
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
        flash("Les deux mots de passe ne sont pas indentiques", "info")
        return render_template('ValidateMail.html', id=id,code=code)
    
    return redirect(url_for('auth.login'))


@auth_blue.route('/accountvalidation<id>', methods=['POST', "GET"])
def account_validation(id):
    code = request.args.get("code")

 
    try:

        user = User.query.filter_by(id=int(id))

        user.filter_by(reset_token=code).update(values={"reset_token":None,
                                                                            "reset_token_expiry":None,
                                                                            "verify_account":True})
        db.session.commit()

        
    except Exception as e:
        return redirect(url_for("home.home"))
    
    try:


        email_receiver = User.query.filter_by(id=int(id)).first().email
        firstname = user.first().firstname
        
        subject = "papagei - Confirmation de création de compte"
        body = f"Bienvenue {str(firstname).capitalize()},\nVotre compte est créé, vous pouvez maintenant vous connecter sur www.papagei-shop.fr pour remplir votre panier.\nÀ très vite,\nL'équipe papagei."

        
        send_mail(body=body,subject=subject, user_mail=email_receiver)

    except Exception as e:
        return redirect(url_for('auth.login'))

    
    return redirect(url_for('auth.login'))