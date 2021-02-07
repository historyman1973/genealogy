from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.fields.html5 import DateField
from genealogy.models import Gender
#
# class AddFather(FlaskForm):
#
#     father_forenames = StringField("Father forenames: ")
#     father_surname = StringField()
#     father_fullname = StringField()
#     father_dob = DateField()
#     fathersubmit = SubmitField("Add")
#
# class AddMother(FlaskForm):
#
#     mother_forenames = StringField("Mother forenames: ")
#     mother_surname = StringField()
#     mother_fullname = StringField()
#     mother_dob = DateField()
#     mothersubmit = SubmitField("Add")
#
# class AddChild(FlaskForm):
#
#     child_forenames = StringField("Child forenames: ")
#     child_surname = StringField()
#     child_fullname = StringField()
#     child_gender = SelectField()
#     child_dob = DateField()
#     childsubmit = SubmitField("Add")



class AddIndividual(FlaskForm):

    grandfather1_forenames = StringField("Father's father: ")
    grandfather1_surname = StringField()
    grandfather1_fullname = StringField()
    grandmother1_forenames = StringField("Father's mother: ")
    grandmother1_surname = StringField()
    grandmother1_fullname = StringField()

    grandfather2_forenames = StringField("Mother's father: ")
    grandfather2_surname = StringField()
    grandmother2_forenames = StringField("Mother's mother: ")
    grandmother2_surname = StringField()

    father_forenames = StringField("Father: ")
    father_surname = StringField()
    father_fullname = StringField()
    father_dob = DateField('dob', format='%Y-%m-%d')

    mother_forenames = StringField("Mother: ")
    mother_surname = StringField()
    mother_fullname = StringField()
    mother_dob = DateField('dob', format='%Y-%m-%d')

    child_forenames = StringField()
    child_surname = StringField()
    child_fullname = StringField()
    child_gender = SelectField(u'Gender', choices=[(choice.name, choice.value) for choice in Gender])
    child_dob = DateField('dob', format='%Y-%m-%d')
