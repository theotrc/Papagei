from flask import render_template, Blueprint, request,redirect, url_for
from ..models import Collection
from flask_login import login_required,current_user
from App import db

collection_blue= Blueprint("collection", __name__, static_folder='../static', template_folder='../templates')





@collection_blue.route('/collections')
@login_required
def collections():
    if current_user.is_admin:
        items = Collection.query.all()
        return render_template("collections.html", items=items)
    else:
        return redirect(url_for("home.home"))

@collection_blue.route('/newcollection')
@login_required
def new():
    if current_user.is_admin:
        return render_template("form_collection.html")
    else:
        return redirect(url_for("home.home"))
    
@collection_blue.route('/newcollection', methods=["POST"])
@login_required
def new_post():
    if current_user.is_admin:
        name = request.form.get('name')
        new_collection = Collection(
                            name=name,
                            x="d"
                                )

            # add the new user to the database
        db.session.add(new_collection)
        db.session.commit()
        
        return redirect(url_for("collection.collections"))
    
    else:
        return redirect(url_for("home.home"))
    
    
@collection_blue.route('/deleteCollection<id>', methods=["POST"])
@login_required
def delete_collection(id):
    if current_user.is_admin:
        print(id)
        # name = request.form.get('name')
        # remove_collection = Collection(
        #                     name=name,
        #                     x="d"
        #                         )

        #     # add the new user to the database
        # db.session.add(remove_collection)
        # db.session.commit()
        
        return redirect(url_for("collection.collections"))
    
    else:
        return redirect(url_for("home.home"))