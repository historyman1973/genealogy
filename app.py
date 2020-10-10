from genealogy import app
from flask import render_template,redirect,url_for
from genealogy import db
from genealogy.models import Individual, Parents
from genealogy.individual.forms import AddIndividual


@app.route("/", methods=["GET", "POST"])
def index():

    form = AddIndividual()

    def fullname(first, last):
        return first + " " + last


    if form.validate_on_submit():
        father_forenames = form.father_forenames.data
        father_surname = form.father_surname.data
        father_fullname = fullname(father_forenames,father_surname)

        mother_forenames = form.mother_forenames.data
        mother_surname = form.mother_surname.data
        mother_fullname = fullname(mother_forenames,mother_surname)

        child_forenames = form.child_forenames.data
        child_surname = form.child_surname.data
        child_fullname = fullname(child_forenames,child_surname)

        new_father = Individual(father_surname, father_fullname, father_forenames)
        new_mother = Individual(mother_surname, mother_fullname, mother_forenames)
        new_child = Individual(child_surname, child_fullname, child_forenames)


        db.session.add(new_father)
        db.session.add(new_mother)
        db.session.add(new_child)

    # flush() writes the parents IDs to the database so we can add them to a Parents object for a given child.
        db.session.flush()

        new_partners = Parents(new_father.id, new_mother.id)
        db.session.add(new_partners)

        new_child.parents.append(new_partners)

        db.session.commit()

        fathername = Individual.query.get(new_child.parents[0].father_id).fullname
        mothername = Individual.query.get(new_child.parents[0].mother_id).fullname
        childname = Individual.query.get(new_child.id).fullname

        return render_template("home.html", form=form, fathername=fathername, mothername=mothername,
                                        childname=childname)

    return render_template("home.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)


# print(david.forenames + "'s father is " + Individual.query.get(david.parents[0].father_id).forenames)