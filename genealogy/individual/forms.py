from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddIndividual(FlaskForm):

    forename = StringField("Name: ")
    middle_name = StringField()
    surname = StringField()
    submit = SubmitField("Add")
