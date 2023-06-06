from flask import render_template, Blueprint


mention_blue= Blueprint("mention", __name__, static_folder='../static', template_folder='../templates')


@mention_blue.route("/mentionslegales")
def mentions_legales():

    
    return render_template("mentions_legales.html")


@mention_blue.route("/cgu")
def cgu():

    
    return render_template("cgu.html")


@mention_blue.route("/cgv")
def cgv():

    
    return render_template("cgv.html")