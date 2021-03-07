from app import app
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from genealogy import db
from genealogy.models import Individual, Parents, FamilyLink, genders
from genealogy.individual.forms import FamilyView, IndividualView, RelationshipView
from genealogy.individual.individual_functions import fullname, link_child, add_father, add_mother, add_patgrandfather, \
    add_patgrandmother, add_matgrandfather, add_matgrandmother, session_pop_grandparents, create_child_partnership, \
    calculate_period, delete_individual

genealogy_blueprint = Blueprint("individual", __name__, template_folder="templates")


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

    parents = Parents.query.get(parentsid)

    children = db.session.query(Individual) \
        .join(FamilyLink) \
        .filter(FamilyLink.parents_id == parentsid) \
        .filter(FamilyLink.individual_id == Individual.id).order_by(Individual.dob)

    number_children = children.count()

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
            add_patgrandfather(form)
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("patgrandfatherfocus") == "focus":
            session_pop_grandparents()

            new_family = Parents.query.filter_by(father_id=patgrandfather.id).first()

            session["partners.id"] = new_family.id
            session["father.id"] = patgrandfather.id
            session["mother.id"] = Parents.query.get(new_family.id).mother_id

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addpatgrandmother") == "Add":
            add_patgrandmother(form)
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("patgrandmotherfocus") == "focus":
            session_pop_grandparents()

            new_family = Parents.query.filter_by(mother_id=patgrandmother.id).first()

            session["partners.id"] = new_family.id
            session["mother.id"] = patgrandmother.id
            session["father.id"] = Parents.query.get(new_family.id).father_id

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addmatgrandfather") == "Add":
            add_matgrandfather(form)
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("matgrandfatherfocus") == "focus":
            session_pop_grandparents()

            new_family = Parents.query.filter_by(father_id=matgrandfather.id).first()

            session["partners.id"] = new_family.id
            session["father.id"] = matgrandfather.id
            session["mother.id"] = Parents.query.get(new_family.id).mother_id

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addmatgrandmother") == "Add":
            add_matgrandmother(form)
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("matgrandmotherfocus") == "focus":
            session_pop_grandparents()

            new_family = Parents.query.filter_by(mother_id=matgrandmother.id).first()

            session["partners.id"] = new_family.id
            session["mother.id"] = matgrandmother.id
            session["father.id"] = Parents.query.get(new_family.id).father_id

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addfather") == "Add":
            add_father(form)
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addmother") == "Add":
            add_mother(form)
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("savemarriage") == "Save":
            parents = Parents.query.get(parentsid)

            parents.dom = form.parents_dom.data
            db.session.commit()
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addrelationship") == "Add":
            parents.dom = form.parents_dom.data

            db.session.commit()
            return redirect(url_for("show_family", parentsid=session["partners.id"]))



        if request.form.get("addchild") == "Add":
            child_forenames = form.child_forenames.data
            child_surname = form.child_surname.data
            child_gender = form.child_gender.data
            child_dob = form.child_dob.data
            child_dod = form.child_dod.data
            child_age = calculate_period(child_dob, child_dod)
            child_fullname = fullname(child_forenames, child_surname)

            new_child = Individual(surname=child_surname, fullname=child_fullname, forenames=child_forenames,
                                   gender=child_gender, dob=child_dob, dod=child_dod, age=child_age)
            db.session.add(new_child)

            db.session.commit()
            db.session.flush()

            session["child.id"] = new_child.id

            link_child(individual_id=session["child.id"], parents_id=session["partners.id"])

            # Handles male and female children only
            create_child_partnership(new_child)

            children = db.session.query(Individual) \
                .join(FamilyLink) \
                .filter(FamilyLink.parents_id == parentsid) \
                .filter(FamilyLink.individual_id == Individual.id).order_by(Individual.dob)

            number_children = children.count()

            return redirect(url_for("show_family", parentsid=session["partners.id"], children=children, father=father,
                                    mother=mother, patgrandfather=patgrandfather, patgrandmother=patgrandmother,
                                    matgrandfather=matgrandfather, matgrandmother=matgrandmother,
                                    number_children=number_children, parents=parents))

        if request.form.get("childfocus"):
            child_id = request.form.get('childfocus')

            if Individual.query.get(child_id).gender == "Male":
                new_family = Parents.query.filter_by(father_id=child_id).first()
                session["partners.id"] = new_family.id
                session["father.id"] = child_id
                session["mother.id"] = Parents.query.get(new_family.id).mother_id
            elif Individual.query.get(child_id).gender == "Female":
                new_family = Parents.query.filter_by(mother_id=child_id).first()
                session["partners.id"] = new_family.id
                session["mother.id"] = child_id
                session["father.id"] = Parents.query.get(new_family.id).father_id
            else:
                flash("Child's gender is unknown, set this first", "error")

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

    return render_template("home.html", form=form, father=father, mother=mother, children=children,
                           patgrandfather=patgrandfather, patgrandmother=patgrandmother, matgrandfather=matgrandfather,
                           matgrandmother=matgrandmother, number_children=number_children, parents=parents)


@app.route("/list", methods=["GET", "POST"])
def individual_list():
    individuals = Individual.query.all()

    return render_template("list.html", individuals=individuals)


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_individual(id):
    form = IndividualView()

    individual = Individual.query.get_or_404(id)

    original_gender = individual.gender

    if request.form.get("saveindividual") == "Save":
        individual.forenames = request.form["individual_forenames"]
        individual.surname = request.form["individual_surname"]
        individual.gender = request.form["individual_gender"]
        individual.dob = form.individual_dob.data
        individual.dod = form.individual_dod.data
        individual.age = calculate_period(individual.dob, individual.dod)

        individual.fullname = fullname(individual.forenames, individual.surname)

        if original_gender == "Unknown" and individual.gender != "Unknown":
            create_child_partnership(individual)

        db.session.commit()

        return redirect(url_for("show_family", parentsid=session["partners.id"]))

    return render_template("edit_individual.html", form=form, individual=individual, genders=genders)


@app.route("/delete/<id>", methods=["GET", "POST"])
def delete(id):

    individual = Individual.query.get_or_404(id)

    if request.form.get("deleteindividual") == "Delete":
        delete_individual(id)

        return redirect(url_for("show_family", parentsid=session["partners.id"]))

    return render_template("delete_individual.html", individual=individual)


@app.route("/editrelationship/<id>", methods=["GET", "POST"])
def edit_relationship(id):
    form = RelationshipView()

    relationship = Parents.query.get_or_404(id)

    if request.form.get("saverelationship") == "Save":
        relationship.dom = form.marriage_date.data

        db.session.commit()

        return redirect(url_for("show_family", parentsid=session["partners.id"]))

    return render_template("edit_relationship.html", form=form, relationship=relationship)
