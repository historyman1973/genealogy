from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.fields.html5 import DateField
from genealogy.models import genders


class FamilyView(FlaskForm):

    patgrandfather_forenames = StringField("Father's father: ")
    patgrandfather_surname = StringField()
    patgrandfather_dob = DateField('dob', format='%Y-%m-%d', default=None)
    patgrandfather_dod = DateField('dod', format='%Y-%m-%d', default=None)
    patgrandmother_forenames = StringField("Father's mother: ")
    patgrandmother_surname = StringField()
    patgrandmother_dob = DateField('dob', format='%Y-%m-%d', default=None)
    patgrandmother_dod = DateField('dod', format='%Y-%m-%d', default=None)

    matgrandfather_forenames = StringField("Father's father: ")
    matgrandfather_surname = StringField()
    matgrandfather_dob = DateField('dob', format='%Y-%m-%d', default=None)
    matgrandfather_dod = DateField('dod', format='%Y-%m-%d', default=None)
    matgrandmother_forenames = StringField("Father's mother: ")
    matgrandmother_surname = StringField()
    matgrandmother_dob = DateField('dob', format='%Y-%m-%d', default=None)
    matgrandmother_dod = DateField('dod', format='%Y-%m-%d', default=None)

    father_forenames = StringField("Father: ")
    father_surname = StringField()
    father_dob = DateField('dob', format='%Y-%m-%d', default="")
    father_dod = DateField('dod', format='%Y-%m-%d', default="")

    mother_forenames = StringField("Mother: ")
    mother_surname = StringField()
    mother_dob = DateField('dob', format='%Y-%m-%d', default=None)
    mother_dod = DateField('dod', format='%Y-%m-%d', default=None)

    child_forenames = StringField()
    child_surname = StringField()
    child_gender = SelectField(u'Gender', choices=[choice for choice in genders])
    child_dob = DateField('dob', format='%Y-%m-%d', default=None)
    child_dod = DateField('dod', format='%Y-%m-%d', default=None)


class IndividualView(FlaskForm):
    individual_forenames = StringField("Father: ")
    individual_surname = StringField()
    individual_gender = SelectField(u'Gender', choices=[choice for choice in genders])
    individual_dob = DateField('dob', format='%Y-%m-%d', default=None)
    individual_dod = DateField('dob', format='%Y-%m-%d', default=None)