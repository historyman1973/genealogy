from genealogy import app
from flask import render_template, session, request
from genealogy import db
from genealogy.models import Individual, Parents, FamilyLink
from genealogy.individual.forms import AddIndividual


@app.route("/", methods=["GET", "POST"])
def index():
    form = AddIndividual()

    def fullname(first, last):
        return first + " " + last

    def create_partners():
        new_parents = Parents(session["new_father.id"], session["new_mother.id"])
        db.session.add(new_parents)
        db.session.commit()
        db.session.flush()

        session["new_partners.id"] = new_parents.id

    def link_child():
        c = FamilyLink(session["new_child.id"], session["new_partners.id"])
        db.session.add(c)
        db.session.commit()
        db.session.flush()

    if request.method == "POST":

        new_father = Individual("", None, None)
        new_mother = Individual("", None, None)
        new_child = Individual("", None, None)
        new_partners = Parents(None, None)

        if request.form.get("addfather") == "Add":
            father_forenames = form.father_forenames.data
            father_surname = form.father_surname.data
            father_fullname = fullname(father_forenames, father_surname)

            new_father = Individual(father_surname, father_fullname, father_forenames)
            db.session.add(new_father)

            db.session.commit()
            db.session.flush()
            session["new_father.id"] = new_father.id
            if form.mother_forenames.data or form.mother_surname.data:
                create_partners()

        if request.form.get("addmother") == "Add":
            mother_forenames = form.mother_forenames.data
            mother_surname = form.mother_surname.data
            mother_fullname = fullname(mother_forenames, mother_surname)

            new_mother = Individual(mother_surname, mother_fullname, mother_forenames)
            db.session.add(new_mother)

            db.session.commit()
            db.session.flush()
            session["new_mother.id"] = new_mother.id
            if form.father_forenames.data or form.father_surname.data:
                create_partners()

        if request.form.get("addchild") == "Add":
            child_forenames = form.child_forenames.data
            child_surname = form.child_surname.data
            child_fullname = fullname(child_forenames, child_surname)

            new_child = Individual(child_surname, child_fullname, child_forenames)
            db.session.add(new_child)

            db.session.commit()
            db.session.flush()

            session["new_child.id"] = new_child.id

            if form.father_forenames.data or form.father_surname.data or form.mother_forenames.data or form.mother_surname.data:
                link_child()

        return render_template("home.html", form=form)

    return render_template("home.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

# print(david.forenames + "'s father is " + Individual.query.get(david.parents[0].father_id).forenames)
