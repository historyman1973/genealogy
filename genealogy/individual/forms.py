from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from genealogy.models import genders
from ..models import Parents, Location


class FamilyView(FlaskForm):

    patgrandfather_forenames = StringField(label="Forenames")
    patgrandfather_surname = StringField(label="Surname")
    patgrandfather_dob = DateField('Born', format='%Y-%m-%d', default=None)
    patgrandfather_dod = DateField('Died', format='%Y-%m-%d', default=None)
    patgrandmother_forenames = StringField(label="Forenames")
    patgrandmother_surname = StringField(label="Surname")
    patgrandmother_dob = DateField('Born', format='%Y-%m-%d', default=None)
    patgrandmother_dod = DateField('Died', format='%Y-%m-%d', default=None)

    matgrandfather_forenames = StringField(label="Forenames")
    matgrandfather_surname = StringField(label="Surname")
    matgrandfather_dob = DateField('Born', format='%Y-%m-%d', default=None)
    matgrandfather_dod = DateField('Died', format='%Y-%m-%d', default=None)
    matgrandmother_forenames = StringField(label="Forenames")
    matgrandmother_surname = StringField(label="Surname")
    matgrandmother_dob = DateField('Born', format='%Y-%m-%d', default=None)
    matgrandmother_dod = DateField('Died', format='%Y-%m-%d', default=None)

    father_forenames = StringField(label="Forenames")
    father_surname = StringField(label="Surname")
    father_dob = DateField('Born', format='%Y-%m-%d', default="")
    father_dod = DateField('Died', format='%Y-%m-%d', default="")

    mother_forenames = StringField(label="Forenames")
    mother_surname = StringField(label="Surname")
    mother_dob = DateField('Born', format='%Y-%m-%d', default=None)
    mother_dod = DateField('Died', format='%Y-%m-%d', default=None)

    parents_dom = DateField("Married", format='%Y-%m-%d', default=None)

    child_forenames = StringField(label="Forenames")
    child_surname = StringField(label="Surname")
    child_gender = SelectField(label='Gender', choices=[choice for choice in genders])
    child_dob = DateField(label='Born', format='%Y-%m-%d', default=None)
    child_dod = DateField(label='Died', format='%Y-%m-%d', default=None)


class IndividualView(FlaskForm):
    individual_forenames = StringField(label="Forenames")
    individual_surname = StringField(label="Surname")
    individual_gender = SelectField(u'Gender', choices=[choice for choice in genders])
    individual_dob = DateField('dob', format='%Y-%m-%d', default=None)
    individual_dod = DateField('dob', format='%Y-%m-%d', default=None)


def location_query():
    return Location.query


def relationshipview_form(relationship_id):
    class RelationshipView(FlaskForm):
        marriage_date = DateField('Date of marriage', format='%Y-%m-%d', default=None)

        # Set the default option of the QuerySelectField to be the current parent's marriage location.
        marriage_location = QuerySelectField(query_factory=location_query, allow_blank=True, get_label="full_location",
                                             default=Location.query.filter_by(id=Parents.query.get(relationship_id).
                                                                              marriage_location).scalar())
        location_address = StringField(label="Address")
        location_parish = StringField(label="Parish")
        location_townorcity = StringField(label="Town or City")
        location_county = StringField(label="County")
        location_country = StringField(label="Country")

    return RelationshipView
