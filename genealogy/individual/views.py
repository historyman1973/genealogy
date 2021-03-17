from app import app
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from genealogy import db
from genealogy.models import Individual, Parents, FamilyLink, genders, Location
from genealogy.individual.forms import familyview_form, IndividualView, individualview_form, relationshipview_form
from genealogy.individual.individual_functions import fullname, link_child, add_father, add_mother, add_patgrandfather, \
    add_patgrandmother, add_matgrandfather, add_matgrandmother, add_child, session_pop_grandparents, \
    create_child_partnership, calculate_period, delete_individual
from ..master_lists.locations import location_formats, add_location

genealogy_blueprint = Blueprint("individual", __name__, template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def index():

    if Parents.query.get(1) is not None:
        return redirect(url_for("show_family", parentsid=1))

    form = IndividualView()    

    if request.form.get("individual_gender") == "Male":
        add_father(form)
        return redirect(url_for("show_family", parentsid=session["partners.id"]))
    elif request.form.get("individual_gender") == "Female":
        add_mother(form)
        return redirect(url_for("show_family", parentsid=session["partners.id"]))

    return render_template("new_family.html", form=form, genders=genders)


@app.route("/family/<parentsid>", methods=["GET", "POST"])
def show_family(parentsid):

    # Grab the Parents object being edited
    parents = Parents.query.get(parentsid)

    # Create the RelationshipView form within a function which sets the default location based on the current parents'
    # marriage location (if it's set) and assign the form to a variable called relationshipview
    familyview = familyview_form(parentsid)

    # Create the standard 'form' variable (for convention) and assign to it the RelationshipView form which now has
    # the relevant default value selected.
    familyform = familyview()

    marriage_location = Location.query.get(parents.marriage_location)

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
            return redirect(url_for("add_individual"))

        if request.form.get("patgrandfatherfocus") == "focus":
            session_pop_grandparents()

            new_family = Parents.query.filter_by(father_id=patgrandfather.id).first()

            session["partners.id"] = new_family.id
            session["father.id"] = patgrandfather.id
            session["mother.id"] = Parents.query.get(new_family.id).mother_id

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addpatgrandmother") == "Add":
            return redirect(url_for("add_individual"))

        if request.form.get("patgrandmotherfocus") == "focus":
            session_pop_grandparents()

            new_family = Parents.query.filter_by(mother_id=patgrandmother.id).first()

            session["partners.id"] = new_family.id
            session["mother.id"] = patgrandmother.id
            session["father.id"] = Parents.query.get(new_family.id).father_id

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addmatgrandfather") == "Add":
            return redirect(url_for("add_individual"))

        if request.form.get("matgrandfatherfocus") == "focus":
            session_pop_grandparents()

            new_family = Parents.query.filter_by(father_id=matgrandfather.id).first()

            session["partners.id"] = new_family.id
            session["father.id"] = matgrandfather.id
            session["mother.id"] = Parents.query.get(new_family.id).mother_id

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addmatgrandmother") == "Add":
            return redirect(url_for("add_individual"))

        if request.form.get("matgrandmotherfocus") == "focus":
            session_pop_grandparents()

            new_family = Parents.query.filter_by(mother_id=matgrandmother.id).first()

            session["partners.id"] = new_family.id
            session["mother.id"] = matgrandmother.id
            session["father.id"] = Parents.query.get(new_family.id).father_id

            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addfather") == "Add":
            add_father(familyform)
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addmother") == "Add":
            add_mother(familyform)
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addchild") == "Add":
            add_child(familyform)

            children = db.session.query(Individual) \
                .join(FamilyLink) \
                .filter(FamilyLink.parents_id == session["partners.id"]) \
                .filter(FamilyLink.individual_id == Individual.id).order_by(Individual.dob)

            number_children = children.count()

            return redirect(url_for("show_family", parentsid=session["partners.id"], children=children, father=father,
                                    mother=mother, patgrandfather=patgrandfather, patgrandmother=patgrandmother,
                                    matgrandfather=matgrandfather, matgrandmother=matgrandmother,
                                    number_children=number_children, parents=parents))

        if request.form.get("savemarriage") == "Save":
            parents = Parents.query.get(parentsid)

            parents.dom = familyform.parents_dom.data
            db.session.commit()
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addrelationship") == "Add":
            parents.dom = familyform.parents_dom.data
            if familyform.parents_marriage_location.data:
                parents.marriage_location = familyform.parents_marriage_location.data.id
            else:
                parents.marriage_location = familyform.parents_marriage_location.data

            db.session.commit()
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addchild") == "Add":
            child_forenames = familyform.child_forenames.data
            child_surname = familyform.child_surname.data
            child_gender = familyform.child_gender.data
            child_dob = familyform.child_dob.data
            if familyform.child_birth_location.data:
                child_birth_location = familyform.child_birth_location.data.id
            else:
                child_birth_location = familyform.child_birth_location.data
            child_dod = familyform.child_dod.data
            if familyform.child_death_location.data:
                child_death_location = familyform.child_death_location.data.id
            else:
                child_death_location = familyform.child_death_location.data

            child_age = calculate_period(child_dob, child_dod)
            child_fullname = fullname(child_forenames, child_surname)

            new_child = Individual(surname=child_surname, fullname=child_fullname, forenames=child_forenames,
                                   gender=child_gender, dob=child_dob, dod=child_dod, age=child_age,
                                   birth_location=child_birth_location, death_location=child_death_location)
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

    return render_template("home.html", form=familyform, father=father, mother=mother, children=children,
                           patgrandfather=patgrandfather, patgrandmother=patgrandmother, matgrandfather=matgrandfather,
                           matgrandmother=matgrandmother, number_children=number_children, parents=parents,
                           marriage_location=marriage_location)


@app.route("/list", methods=["GET", "POST"])
def individual_list():
    individuals = Individual.query.all()

    return render_template("list.html", individuals=individuals)


@app.route("/add/<role>", methods=["GET", "POST"])
def add_individual(role):

    edit_individual = False

    form = IndividualView()

    if request.form.get("saveindividual") == "Save":
        if role == "patgrandfather":
            add_patgrandfather(form)
        elif role == "patgrandmother":
            add_patgrandmother(form)
        elif role == "matgrandfather":
            add_matgrandfather(form)
        elif role == "matgrandmother":
            add_matgrandmother(form)
        elif role == "father":
            add_father(form)
        elif role == "mother":
            add_mother(form)
        elif role == "child":
            add_child(form)

        return redirect(url_for("show_family", parentsid=session["partners.id"]))

    if request.form.get("addlocation") == "Add":
        add_location(form)

    return render_template("edit_individual.html", form=form, genders=genders, edit_individual=edit_individual,
                           role=role)


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_individual(id):

    edit_individual = True

    individual = Individual.query.get_or_404(id)

    individualview = individualview_form(id)

    form = individualview()

    original_gender = individual.gender

    if request.form.get("saveindividual") == "Save":
        individual.forenames = form.individual_forenames.data
        individual.surname = form.individual_surname.data
        individual.gender = form.individual_gender.data
        individual.dob = form.individual_dob.data
        if form.individual_birth_location.data:
            individual.birth_location = form.individual_birth_location.data.id
        else:
            individual.birth_location = form.individual_birth_location.data
        individual.dod = form.individual_dod.data
        if form.individual_death_location.data:
            individual.death_location = form.individual_death_location.data.id
        else:
            individual.death_location = form.individual_death_location.data
        individual.age = calculate_period(individual.dob, individual.dod)

        individual.fullname = fullname(individual.forenames, individual.surname)

        if original_gender == "Unknown" and individual.gender != "Unknown":
            create_child_partnership(individual)

        db.session.commit()

        return redirect(url_for("show_family", parentsid=session["partners.id"]))

    if request.form.get("addlocation") == "Add":
        add_location(form)

    return render_template("edit_individual.html", form=form, individual=individual, genders=genders,
                           edit_individual=edit_individual)


@app.route("/delete/<id>", methods=["GET", "POST"])
def delete(id):

    individual = Individual.query.get_or_404(id)

    if request.form.get("deleteindividual") == "Delete":
        delete_individual(id)

        return redirect(url_for("show_family", parentsid=session["partners.id"]))

    return render_template("delete_individual.html", individual=individual)


@app.route("/editrelationship/<id>", methods=["GET", "POST"])
def edit_relationship(id):

    # Grab the Parents object being edited
    relationship = Parents.query.get_or_404(id)

    # Create the RelationshipView form within a function which sets the default location based on the current parents'
    # marriage location (if it's set) and assign the form to a variable called relationshipview
    relationshipview = relationshipview_form(id)

    # Create the standard 'form' variable (for convention) and assign to it the RelationshipView form which now has
    # the relevant default value selected.
    form = relationshipview()

    if request.form.get("saverelationship") == "Save":
        relationship.dom = form.marriage_date.data
        if form.marriage_location.data:
            relationship.marriage_location = form.marriage_location.data.id
        else:
            relationship.marriage_location = form.marriage_location.data

        db.session.commit()

        return redirect(url_for("show_family", parentsid=session["partners.id"]))

    if request.form.get("addlocation") == "Add":
        add_location(form)
        
        # address = form.location_address.data
        # parish = form.location_parish.data
        # district = form.location_district.data
        # townorcity = form.location_townorcity.data
        # county = form.location_county.data
        # country = form.location_country.data
        # full_location = location_formats("long", address, parish, district, townorcity, county, country)
        # short_location = location_formats("short", parish, townorcity, county)
        # 
        # new_location = Location(address=address, parish=parish, district=district, townorcity=townorcity,
        #                         county=county, country=country, full_location=full_location,
        #                         short_location=short_location)
        # 
        # db.session.add(new_location)
        # db.session.commit()

    return render_template("edit_relationship.html", form=form, relationship=relationship)
