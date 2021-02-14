from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.fields.html5 import DateField
from genealogy.models import Gender


class FamilyView(FlaskForm):

    patgrandfather_forenames = StringField("Father's father: ")
    patgrandfather_surname = StringField()
    patgrandfather_dob = DateField('dob', format='%Y-%m-%d')
    patgrandmother_forenames = StringField("Father's mother: ")
    patgrandmother_surname = StringField()
    patgrandmother_dob = DateField('dob', format='%Y-%m-%d')

    matgrandfather_forenames = StringField("Mother's father: ")
    matgrandfather_surname = StringField()
    matgrandfather_dob = DateField('dob', format='%Y-%m-%d')
    matgrandmother_forenames = StringField("Mother's mother: ")
    matgrandmother_surname = StringField()
    matgrandmother_dob = DateField('dob', format='%Y-%m-%d')

    father_forenames = StringField("Father: ")
    father_surname = StringField()
    father_dob = DateField('dob', format='%Y-%m-%d')

    mother_forenames = StringField("Mother: ")
    mother_surname = StringField()
    mother_dob = DateField('dob', format='%Y-%m-%d')

    child_forenames = StringField()
    child_surname = StringField()
    child_gender = SelectField(u'Gender', choices=[(choice.name, choice.value) for choice in Gender])
    child_dob = DateField('dob', format='%Y-%m-%d')
