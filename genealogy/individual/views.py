from flask import Blueprint,render_template,redirect,url_for
from genealogy import db
from genealogy.models import Individual, Parents
from genealogy.individual.forms import FamilyView
# from genealogy.individual.forms import AddFather, AddMother, AddChild

genealogy_blueprint = Blueprint("individual",__name__,
                template_folder="templates")

# @genealogy_blueprint.route("/",methods=["GET","POST"])
# def index():
#
#     form = AddIndividual()
#
#     if form.child_submit():
#         forenames = form.child_forenames.data
#         surname = form.child_surname.data
#
#         new_individual = Individual(surname, forenames)
#         db.session.add(new_individual)
#         db.session.commit()
#
#         return redirect(url_for("index"))
#     return render_template("home.html", form=form)
