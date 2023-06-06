from flask import render_template, Blueprint


contact_blue= Blueprint("contact", __name__, static_folder="../static", template_folder="../templates")

@contact_blue.route("/contact")
def contact():
    return render_template("contact.html")

