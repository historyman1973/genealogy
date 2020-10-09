from flask import Blueprint,render_template,redirect,url_for
from genealogy import db
from genealogy.models import Individual, Parents
from genealogy.individual.forms import AddIndividual

genealogy_blueprint = Blueprint("individual",__name__,
                template_folder="templates")

# @genealogy_blueprint.route("/",methods=["GET","POST"])
# def index():
#
#     form = AddIndividual()
#
#     if form.child_submit():
#         forename = form.child_forename.data
#         middle_name = form.child_middle_name.data
#         surname = form.child_surname.data
#
#         new_individual = Individual(surname, forename, middle_name)
#         db.session.add(new_individual)
#         db.session.commit()
#
#         return redirect(url_for("index"))
#     return render_template("home.html", form=form)
