from genealogy import app
from flask import render_template,redirect,url_for
from genealogy import db
from genealogy.models import Individual, Parents
from genealogy.individual.forms import AddIndividual

@app.route("/", methods=["GET", "POST"])
def index():
# New comment
    form = AddIndividual()

    if form.validate_on_submit():
        forename = form.forename.data
        middle_name = form.middle_name.data
        surname = form.surname.data

        new_individual = Individual(surname, forename, middle_name)
        db.session.add(new_individual)
        db.session.commit()


        return redirect(url_for("index"))
    return render_template("home.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
