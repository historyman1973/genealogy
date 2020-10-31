from genealogy import app
from flask import render_template, session, request
from genealogy import db
from genealogy.models import Individual, Parents, FamilyLink
from genealogy.individual.forms import AddIndividual


@app.route("/", methods=["GET", "POST"])
def index():
    form = AddIndividual()

    father_fullname = None
    mother_fullname = None
    focus_father = None
    focus_mother = None

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

    def update_partners(partners_id, father_id=None, mother_id=None):

        if db.session.query(Parents).filter_by(id=partners_id, father_id=father_id).scalar() is None:
            # print("Running update partner, partners ID is " + str(partners_id) + " and father ID is " + str(father_id))
            updated_father = db.session.query(Parents).get(partners_id)
            # print("Partner ID: " + str(updated_father.id) + ", Father ID: " + str(updated_father.father_id) + ", Mother ID: " + str(updated_father.mother_id))
            updated_father.father_id = session["father.id"]
            db.session.commit()
            db.session.flush()
        elif db.session.query(Parents).filter_by(id=partners_id, mother_id=mother_id).scalar() is None:
            print("Running update partner, partners ID is " + str(partners_id) + " and mother ID is " + str(mother_id))
            updated_mother = db.session.query(Parents).get(partners_id)
            updated_mother.mother_id = session["mother.id"]
            db.session.commit()
            db.session.flush()

    def link_child(individual_id, parents_id):
        if db.session.query(FamilyLink).filter_by(individual_id=individual_id,
                                                       parents_id=parents_id).scalar() is None:
            c = FamilyLink(individual_id, parents_id)
            db.session.add(c)
            db.session.commit()
            db.session.flush()

    if request.method == "POST":

        if request.form.get("addgrandfather1") == "Add":
            grandfather1_forenames = form.grandfather1_forenames.data
            grandfather1_surname = form.grandfather1_surname.data
            grandfather1_fullname = fullname(grandfather1_forenames, grandfather1_surname)

            grandfather1 = Individual(grandfather1_surname, grandfather1_fullname, grandfather1_forenames)
            db.session.add(grandfather1)

            db.session.commit()
            db.session.flush()
            session["father.id"] = grandfather1.id
            session["grandfather1_fullname"] = grandfather1_fullname

            if form.grandmother1_forenames.data or form.grandmother1_surname.data:
                create_partners()


        if request.form.get("addfather") == "Add":
            father_forenames = form.father_forenames.data
            father_surname = form.father_surname.data
            father_fullname = fullname(father_forenames, father_surname)

            new_father = Individual(father_surname, father_fullname, father_forenames)
            db.session.add(new_father)

            db.session.commit()
            db.session.flush()
            session["father.id"] = new_father.id
            session["father_fullname"] = father_fullname
            # Enable following line if father is added first
            # session["mother.id"] = None
            focus_father = new_father

            if session.get("mother.id") is not None:
                update_partners(partners_id=session["partners.id"], father_id=session["father.id"],
                                mother_id=session["mother.id"])
            else:
                create_partners(father_id=session["father.id"])


        if request.form.get("addmother") == "Add":
            mother_forenames = form.mother_forenames.data
            mother_surname = form.mother_surname.data
            mother_fullname = fullname(mother_forenames, mother_surname)

            new_mother = Individual(mother_surname, mother_fullname, mother_forenames)
            db.session.add(new_mother)

            db.session.commit()
            db.session.flush()
            session["mother.id"] = new_mother.id
            session["mother_fullname"] = mother_fullname
            # Enable following line if mother added first
            # session["father.id"] = None
            focus_mother = new_mother

            if session.get("father.id") is not None:
                update_partners(partners_id=session["partners.id"], father_id=session["father.id"],
                                mother_id=session["mother.id"])
            else:
                create_partners(mother_id=session["mother.id"])

        if request.form.get("addchild") == "Add":
            child_forenames = form.child_forenames.data
            child_surname = form.child_surname.data
            child_fullname = fullname(child_forenames, child_surname)

            new_child = Individual(child_surname, child_fullname, child_forenames)
            db.session.add(new_child)

            db.session.commit()
            db.session.flush()

            session["child.id"] = new_child.id

            if form.father_forenames.data or form.father_surname.data or form.mother_forenames.data or form.mother_surname.data:
                link_child()

        return render_template("home.html", form=form, father_fullname=father_fullname, mother_fullname=mother_fullname)

    return render_template("home.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

# print(david.forenames + "'s father is " + Individual.query.get(david.parents[0].father_id).forenames)