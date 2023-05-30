from flask import render_template, Blueprint



papagei_blue= Blueprint("papagei", __name__, static_folder='../static', template_folder='../templates')


@papagei_blue.route("/")
def papagei():
    
    return render_template("papagei.html")