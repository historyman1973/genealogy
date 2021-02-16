from app import app
from flask import Blueprint,render_template,redirect,url_for,session,request
from genealogy import db
from genealogy.models import Individual, Parents, FamilyLink
from genealogy.individual.forms import FamilyView
from genealogy.individual.individual_functions import fullname, link_child, add_father, add_mother, add_patGrandfather,\
    add_patGrandmother, add_matGrandfather, add_matGrandmother

genealogy_blueprint = Blueprint("individual",__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def index():
    form = FamilyView()

    if Parents.query.get(1) is not None:
        return redirect(url_for("show_family", parentsid=1))

    if request.method == "POST":

        if request.form.get("addfather") == "Add":
            add_father(form)

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addmother") == "Add":
            add_mother(form)

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

    return render_template("home.html", form=form)


@app.route("/family/<parentsid>", methods=["GET", "POST"])
def show_family(parentsid):
    form = FamilyView()

    children = db.session.query(Individual) \
        .join(FamilyLink) \
        .filter(FamilyLink.parents_id == parentsid) \
        .filter(FamilyLink.individual_id == Individual.id)

    try:
        father = Individual.query.get(Parents.query.get(parentsid).father_id)
    except:
        father = None

    try:
        mother = Individual.query.get(Parents.query.get(parentsid).mother_id)
    except:
        mother = None

    try:
        patgrandfather = Individual.query.get(
            Individual.query.get(Parents.query.get(parentsid).father_id).parents[0].father_id)
    except:
        patgrandfather = None

    try:
        patgrandmother = Individual.query.get(
            Individual.query.get(Parents.query.get(parentsid).father_id).parents[0].mother_id)
    except:
        patgrandmother = None

    try:
        matgrandfather = Individual.query.get(
            Individual.query.get(Parents.query.get(parentsid).mother_id).parents[0].father_id)
    except:
        matgrandfather = None

    try:
        matgrandmother = Individual.query.get(
            Individual.query.get(Parents.query.get(parentsid).mother_id).parents[0].mother_id)
    except:
        matgrandmother = None

    if request.method == "POST":

        if request.form.get("addpatgrandfather") == "Add":
            add_patGrandfather(form)

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addpatgrandmother") == "Add":
            add_patGrandmother(form)

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addmatgrandfather") == "Add":
            add_matGrandfather(form)

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addmatgrandmother") == "Add":
            add_matGrandmother(form)

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addfather") == "Add":
            add_father(form)

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addmother") == "Add":
            add_mother(form)

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addchild") == "Add":
            child_forenames = form.child_forenames.data
            child_surname = form.child_surname.data
            child_gender = form.child_gender.data
            child_dob = form.child_dob.data
            child_fullname = fullname(child_forenames, child_surname)

            new_child = Individual(child_surname, child_fullname, child_forenames, child_gender, child_dob)
            db.session.add(new_child)

            db.session.commit()
            db.session.flush()

            session["child.id"] = new_child.id

            link_child(individual_id=session["child.id"], parents_id=session["partners.id"])

            children = db.session.query(Individual) \
                .join(FamilyLink) \
                .filter(FamilyLink.parents_id == parentsid) \
                .filter(FamilyLink.individual_id == Individual.id)

            form.child_forenames.data = ""

            return redirect(url_for("show_family", parentsid=session["partners.id"], children=children, father=father,
                                    mother=mother,
                                    patgrandfather=patgrandfather, patGrandmother=patgrandmother,
                                    matGrandfather=matgrandfather,
                                    matGrandmother=matgrandmother))

    return render_template("home.html", form=form, father=father, mother=mother, children=children,
                           patgrandfather=patgrandfather, patgrandmother=patgrandmother, matgrandfather=matgrandfather,
                           matgrandmother=matgrandmother)

@app.route("/list", methods=["GET", "POST"])
def individual_list():
    individuals = Individual.query.all()

    return render_template("list.html", individuals=individuals)