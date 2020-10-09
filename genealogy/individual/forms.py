from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AddIndividual(FlaskForm):

    father_forename = StringField("Father Name: ")
    father_middle_name = StringField()
    father_surname = StringField()
    mother_forename = StringField("Mother Name: ")
    mother_middle_name = StringField()
    mother_surname = StringField()
    child_forename = StringField("Child Name: ")
    child_middle_name = StringField()
    child_surname = StringField()
    submit = SubmitField(label="Add Child")
