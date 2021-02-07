from genealogy import app
from flask import render_template, session, request, redirect, url_for
from genealogy import db
from genealogy.models import Individual, Parents, FamilyLink, Gender
from genealogy.individual.forms import AddIndividual


@app.route("/", methods=["GET", "POST"])
def index():
    form = AddIndividual()

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
    form = AddIndividual()

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


    if request.method == "POST":

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

            return redirect(url_for("show_family", parentsid=session["partners.id"], children=children))

    return render_template("home.html", form=form, father=father, mother=mother, children=children)


def fullname(first, last):
    return first + " " + last


def create_partners(father_id=None, mother_id=None):
    if db.session.query(Parents).filter_by(father_id=father_id,
                                           mother_id=mother_id).scalar() is None:
        parents = Parents(father_id, mother_id)
        db.session.add(parents)
        db.session.commit()
        db.session.flush()

        session["partners.id"] = parents.id
        parentsid = parents.id
        return parentsid


def update_partners(partners_id, father_id=None, mother_id=None):
    if db.session.query(Parents).filter_by(id=partners_id, father_id=father_id).scalar() is None:
        updated_father = db.session.query(Parents).get(partners_id)
        parentsid = session["partners.id"]
        updated_father.father_id = session["father.id"]
        db.session.commit()
        db.session.flush()
        return parentsid
    elif db.session.query(Parents).filter_by(id=partners_id, mother_id=mother_id).scalar() is None:
        updated_mother = db.session.query(Parents).get(partners_id)
        parentsid = session["partners.id"]
        updated_mother.mother_id = session["mother.id"]
        db.session.commit()
        db.session.flush()
        return parentsid


def link_child(individual_id, parents_id):
    if db.session.query(FamilyLink).filter_by(individual_id=individual_id,
                                              parents_id=parents_id).scalar() is None:
        c = FamilyLink(individual_id, parents_id)
        db.session.add(c)
        db.session.commit()
        db.session.flush()


def add_father(form):
    father_forenames = form.father_forenames.data
    father_surname = form.father_surname.data
    father_gender = Gender.male
    father_dob = form.father_dob.data
    father_fullname = fullname(father_forenames, father_surname)

    new_father = Individual(father_surname, father_fullname, father_forenames, father_gender, father_dob)
    db.session.add(new_father)

    db.session.commit()
    db.session.flush()

    session["father.id"] = new_father.id
    session["father_fullname"] = father_fullname

    if session.get("mother.id") is None:
        create_partners(father_id=session["father.id"], mother_id=None)
    else:
        update_partners(partners_id=session["partners.id"], father_id=session["father.id"],
                        mother_id=session["mother.id"])

    return


def add_mother(form):
    mother_forenames = form.mother_forenames.data
    mother_surname = form.mother_surname.data
    mother_gender = Gender.female
    mother_dob = form.mother_dob.data
    mother_fullname = fullname(mother_forenames, mother_surname)

    new_mother = Individual(mother_surname, mother_fullname, mother_forenames, mother_gender, mother_dob)
    db.session.add(new_mother)

    db.session.commit()
    db.session.flush()
    session["mother.id"] = new_mother.id

    if session.get("father.id") is None:
        create_partners(father_id=None, mother_id=session["mother.id"])
    else:
        update_partners(partners_id=session["partners.id"], father_id=session["father.id"],
                        mother_id=session["mother.id"])

    return


if __name__ == "__main__":
    app.run(debug=True)
