from flask import render_template, Blueprint


news_blue= Blueprint("news", __name__, static_folder="../static", template_folder="../templates")


@news_blue.route("/news")
def news():
    return render_template("news.html")
