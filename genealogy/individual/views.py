import os

from werkzeug.utils import secure_filename

from app import app
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from genealogy import db, photos
from genealogy.models import Individual, Parents, FamilyLink, genders, Location, Image, IndividualImageLink
from genealogy.individual.forms import familyview_form, IndividualView, individualview_form, RelationshipView, \
    relationshipview_form, ImageUpload
from genealogy.individual.individual_functions import fullname, link_child, add_father, add_mother, add_patgrandfather, \
    add_patgrandmother, add_matgrandfather, add_matgrandmother, add_partner, add_child, session_pop_grandparents, \
    create_child_partnership, calculate_period, delete_individual, add_person
from ..master_lists.locations import add_location

genealogy_blueprint = Blueprint("individual", __name__, template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def index():

    if Parents.query.get(1) is not None:
        return redirect(url_for("show_family", parentsid=session["partners.id"]))

    form = IndividualView()    

    if request.form.get("individual_gender") == "Male":
        add_person(form, role="father")
        add_father()
        return redirect(url_for("show_family", parentsid=session["partners.id"]))
    elif request.form.get("individual_gender") == "Female":
        add_person(form, role="mother")
        add_mother()
        return redirect(url_for("show_family", parentsid=session["partners.id"]))

    return render_template("new_family.html", form=form, genders=genders)


@app.route("/family/<parentsid>", methods=["GET", "POST"])
def show_family(parentsid):

    # Grab the Parents object being edited
    parents = Parents.query.get(parentsid)
    session["partners.id"] = parents.id

    # Create the RelationshipView form within a function which sets the default location based on the current parents'
    # marriage location (if it's set) and assign the form to a variable called relationshipview
    familyview = familyview_form(parents.id)

    # Create the standard 'form' variable (for convention) and assign to it the RelationshipView form which now has
    # the relevant default value selected.
    familyform = familyview()

    # marriage_location = Location.query.get(parents.marriage_location)
    marriage_location = Location.query.get(parents.marriage_location)

    children = db.session.query(Individual) \
        .join(FamilyLink) \
        .filter(FamilyLink.parents_id == parents.id) \
        .filter(FamilyLink.individual_id == Individual.id).order_by(Individual.dob)

    number_children = children.count()

    try:
        father = Individual.query.get(Parents.query.get(parents.id).father_id)
        session["father.id"] = father.id
    except:
        father = None

    try:
        mother = Individual.query.get(Parents.query.get(parents.id).mother_id)
        session["mother.id"] = mother.id
    except:
        mother = None

    try:
        patgrandfather = Individual.query.get(
            Individual.query.get(Parents.query.get(parentsid).father_id).parents[0].father_id)
        session["patgrandfather.id"] = patgrandfather.id
    except:
        patgrandfather = None

    try:
        patgrandmother = Individual.query.get(
            Individual.query.get(Parents.query.get(parentsid).father_id).parents[0].mother_id)
        session["patgrandmother.id"] = patgrandmother.id
    except:
        patgrandmother = None

    try:
        matgrandfather = Individual.query.get(
            Individual.query.get(Parents.query.get(parentsid).mother_id).parents[0].father_id)
        session["matgrandfather.id"] = matgrandfather.id
    except:
        matgrandfather = None

    try:
        matgrandmother = Individual.query.get(
            Individual.query.get(Parents.query.get(parentsid).mother_id).parents[0].mother_id)
        session["matgrandmother.id"] = matgrandmother.id
    except:
        matgrandmother = None

    if father:
        fatherspartners = db.session.query(Parents).filter(Parents.father_id == session["father.id"])
    else:
        fatherspartners = None

    if mother:
        motherspartners = db.session.query(Parents).filter(Parents.mother_id == session["mother.id"])
    else:
        motherspartners = None

    fatherotherfamilies = {}
    if session.get("father.id"):
        fatherfamilies = db.session.query(Parents).filter(Parents.father_id == session["father.id"]).\
        filter(Parents.id != parents.id).all()
        for fatherfamily in fatherfamilies:
            fatherotherfamilies[fatherfamily] = db.session.query(Individual).join(FamilyLink).\
            filter(FamilyLink.parents_id == fatherfamily.id).filter(FamilyLink.individual_id).order_by(Individual.dob)
            print(fatherfamily)

    motherotherfamilies = {}
    if session.get("mother.id"):
        motherfamilies = db.session.query(Parents).filter(Parents.mother_id == session["mother.id"]).\
            filter(Parents.id != parents.id).all()
        for motherfamily in motherfamilies:
            motherotherfamilies[motherfamily] = db.session.query(Individual).join(FamilyLink).\
            filter(FamilyLink.parents_id == motherfamily.id).filter(FamilyLink.individual_id).order_by(Individual.dob)
            print(motherfamily)

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
            add_father()
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addmother") == "Add":
            add_mother()
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

        if request.form.get("addchild") == "Add":
            add_child()

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
            # parents = Parents.query.get(parentsid)
            parents = Parents.query.get(parents.id)

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
                .filter(FamilyLink.parents_id == parents.id) \
                .filter(FamilyLink.individual_id == Individual.id).order_by(Individual.dob)

            number_children = children.count()

            return redirect(url_for("show_family", parentsid=session["partners.id"], children=children, father=father,
                                    mother=mother, patgrandfather=patgrandfather, patgrandmother=patgrandmother,
                                    matgrandfather=matgrandfather, matgrandmother=matgrandmother,
                                    number_children=number_children, parents=parents,
                                    fatherotherfamilies=fatherotherfamilies, motherotherfamilies=motherotherfamilies))

        if request.form.get("childfocus"):
            child_id = request.form.get('childfocus')

            if Individual.query.get(child_id).gender == "Male":
                new_family = Parents.query.filter_by(father_id=child_id).first()
                session["partners.id"] = new_family.id
                session["father.id"] = child_id
                session["mother.id"] = Parents.query.get(new_family.id).mother_id
                print("Session mother.id is " + str(session["mother.id"]))
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
                           marriage_location=marriage_location, fatherspartners=fatherspartners,
                           motherspartners=motherspartners, fatherotherfamilies=fatherotherfamilies,
                           motherotherfamilies=motherotherfamilies)


@app.route("/individuals", methods=["GET", "POST"])
def individual_list():
    individuals = Individual.query.all()

    return render_template("individuals.html", individuals=individuals)


@app.route("/locations", methods=["GET", "POST"])
def location_list():
    locations = db.session.query(Location).order_by(Location.townorcity)

    return render_template("locations.html", locations=locations)


@app.route("/uploadimage", methods=["POST"])
def upload_image():
    return render_template("uploadimage.html")


@app.route("/add/<role>", methods=["GET", "POST"])
def add_individual(role):

    edit_individual = False

    form = IndividualView()

    if request.form.get("saveindividual") == "Save":

        # Pass the role along with the form to the general add_person() function (so the gender can be defined)
        add_person(form, role)

        if role == "patgrandfather":
            add_patgrandfather()
        elif role == "patgrandmother":
            add_patgrandmother()
        elif role == "matgrandfather":
            add_matgrandfather()
        elif role == "matgrandmother":
            add_matgrandmother()
        elif role == "father":
            add_father()
        elif role == "mother":
            add_mother()
        elif role == "fatherspartner":
            add_partner("father")
        elif role == "motherspartner":
            add_partner("mother")
        elif role == "child":
            add_child()

        return redirect(url_for("show_family", parentsid=session["partners.id"]))

    if request.form.get("addlocation") == "Add":
        add_location(form)


    return render_template("edit_individual.html", form=form, genders=genders, edit_individual=edit_individual,
                           role=role)


@app.route("/edit/<context>/<id>", methods=["GET", "POST"])
def edit_individual(context, id):

    edit_individual = True

    individual = Individual.query.get_or_404(id)

    individualview = individualview_form(id)

    form = individualview()

    original_gender = individual.gender

    photo_query = db.session.query(Image).join(IndividualImageLink).filter(IndividualImageLink.individual_id == id)
    if photo_query.count == 1:
        preferred_photo = photo_query.first()
    elif photo_query.count == 0:
        preferred_photo = None
    else:
        preferred_photo = Individual.query.get(id).preferred_image
    photos = photo_query.all()

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
        individual.preferred_image = request.form["pref_photos"]
        individual.age = calculate_period(individual.dob, individual.dod)

        individual.fullname = fullname(individual.forenames, individual.surname)

        if original_gender == "Unknown" and individual.gender != "Unknown":
            create_child_partnership(individual)

        db.session.commit()

        if context == "indlist":
            individuals = Individual.query.all()
            return render_template("individuals.html", individuals=individuals)
        elif context == "familyview":
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

    if request.form.get("addlocation") == "Add":
        add_location(form)

    if request.form.get("cancelindividual") == "Cancel":
        if context == "indlist":
            individuals = Individual.query.all()
            return render_template("individuals.html", individuals=individuals)
        elif context == "familyview":
            return redirect(url_for("show_family", parentsid=session["partners.id"]))

    return render_template("edit_individual.html", form=form, individual=individual, genders=genders,
                           edit_individual=edit_individual, preferred_photo=preferred_photo, photos=photos)


@app.route("/addphoto/<id>", methods=["GET", "POST"])
def add_photo(id):
    form = ImageUpload()

    if request.form.get("addphoto") == "Add":

        new_image_description = form.description.data
        new_image_year = form.year.data

        filename = secure_filename(form.photo.data.filename)                           #
        form.photo.data.save('genealogy/static/photos/' + filename)

        new_image = Image(imageyear=new_image_year, imagedesc=new_image_description, imagepath=filename)

        db.session.add(new_image)
        db.session.commit()
        db.session.flush()

        l = IndividualImageLink(individual_id=id, image_id=new_image.id)

        db.session.add(l)
        db.session.commit()
        db.session.flush()

        photo_query = db.session.query(Image).join(IndividualImageLink).filter(IndividualImageLink.individual_id == id)
        if photo_query.count() == 1:
            Individual.query.get_or_404(id).preferred_image = new_image.id

        return redirect(url_for("edit_individual", context="familyview", id=id))

    return render_template("upload_image.html", id=id, form=form)


@app.route("/delete/<id>", methods=["GET", "POST"])
def delete(id):

    individual = Individual.query.get_or_404(id)

    if request.form.get("deleteindividual") == "Delete":
        delete_individual(id)

        return redirect(url_for("show_family", parentsid=session["partners.id"]))

    return render_template("delete_individual.html", individual=individual)


@app.route("/addrelationship/<id>", methods=["GET", "POST"])
def add_relationship(id):

    # Grab the Parents object being edited
    relationship = Parents.query.get_or_404(id)

    # Create the standard 'form' variable (for convention) and assign to it the RelationshipView form which now has
    # the relevant default value selected.
    form = RelationshipView()

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

        form.marriage_location.data = Location.query.get(session["new_location_id"])
        session.pop("new_location.id", None)

    return render_template("edit_relationship.html", form=form, relationship=relationship)


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

        form.marriage_location.data = Location.query.get(session["new_location_id"])
        session.pop("new_location.id", None)

    return render_template("edit_relationship.html", form=form, relationship=relationship)
