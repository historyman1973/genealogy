from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AddIndividual(FlaskForm):

    father_forenames = StringField("Father forenames: ")
    father_surname = StringField()
    mother_forenames = StringField("Mother forenames: ")
    mother_surname = StringField()
    child_forenames = StringField("Child forenames: ")
    child_surname = StringField()
    submit = SubmitField(label="Add Child")
