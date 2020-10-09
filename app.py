from genealogy import app
from flask import render_template,redirect,url_for
from genealogy import db
from genealogy.models import Individual, Parents
from genealogy.individual.forms import AddIndividual


@app.route("/", methods=["GET", "POST"])
def index():

    form = AddIndividual()

    if form.validate_on_submit():
        father_forename = form.father_forename.data
        father_middle_name = form.father_middle_name.data
        father_surname = form.father_surname.data
        mother_forename = form.mother_forename.data
        mother_middle_name = form.mother_middle_name.data
        mother_surname = form.mother_surname.data
        child_forename = form.child_forename.data
        child_middle_name = form.child_middle_name.data
        child_surname = form.child_surname.data

        new_father = Individual(father_surname, father_forename, father_middle_name)
        new_mother = Individual(mother_surname, mother_forename, mother_middle_name)
        new_child = Individual(child_surname, child_forename, child_middle_name)


        db.session.add(new_father)
        db.session.add(new_mother)
        db.session.add(new_child)

    # flush() writes the parents IDs to the database so we can add them to a Parents object for a given child.
        db.session.flush()

        new_partners = Parents(new_father.id, new_mother.id)
        db.session.add(new_partners)

        new_child.parents.append(new_partners)

        db.session.commit()

        return redirect(url_for("index"))

    return render_template("home.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)


# print(david.forename + "'s father is " + Individual.query.get(david.parents[0].father_id).forename)