from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from genealogy.models import genders
from ..models import Individual, Parents, Location


def location_query():
    return Location.query


def familyview_form(relationship_id):
    class FamilyView(FlaskForm):

        patgrandfather_forenames = StringField(label="Forenames")
        patgrandfather_surname = StringField(label="Surname")
        patgrandfather_dob = DateField('Born', format='%Y-%m-%d', default=None)
        patgrandfather_birth_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                         get_label="full_location")
        patgrandfather_dod = DateField('Died', format='%Y-%m-%d', default=None)
        patgrandfather_death_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                         get_label="full_location")
        ################################################################################################################
        patgrandmother_forenames = StringField(label="Forenames")
        patgrandmother_surname = StringField(label="Surname")
        patgrandmother_dob = DateField('Born', format='%Y-%m-%d', default=None)
        patgrandmother_birth_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                           get_label="full_location")
        patgrandmother_dod = DateField('Died', format='%Y-%m-%d', default=None)
        patgrandmother_death_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                           get_label="full_location")
        ################################################################################################################
        matgrandfather_forenames = StringField(label="Forenames")
        matgrandfather_surname = StringField(label="Surname")
        matgrandfather_dob = DateField('Born', format='%Y-%m-%d', default=None)
        matgrandfather_birth_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                         get_label="full_location")
        matgrandfather_dod = DateField('Died', format='%Y-%m-%d', default=None)
        matgrandfather_death_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                         get_label="full_location")
        ################################################################################################################
        matgrandmother_forenames = StringField(label="Forenames")
        matgrandmother_surname = StringField(label="Surname")
        matgrandmother_dob = DateField('Born', format='%Y-%m-%d', default=None)
        matgrandmother_birth_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                         get_label="full_location")
        matgrandmother_dod = DateField('Died', format='%Y-%m-%d', default=None)
        matgrandmother_death_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                         get_label="full_location")
        ################################################################################################################
        father_forenames = StringField(label="Forenames")
        father_surname = StringField(label="Surname")
        father_dob = DateField('Born', format='%Y-%m-%d', default="")
        father_birth_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                         get_label="full_location")
        father_dod = DateField('Died', format='%Y-%m-%d', default="")
        father_death_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                         get_label="full_location")
        ################################################################################################################
        mother_forenames = StringField(label="Forenames")
        mother_surname = StringField(label="Surname")
        mother_dob = DateField('Born', format='%Y-%m-%d', default=None)
        mother_birth_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                 get_label="full_location")
        mother_dod = DateField('Died', format='%Y-%m-%d', default=None)
        mother_death_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                 get_label="full_location")
        ################################################################################################################
        parents_dom = DateField("Married", format='%Y-%m-%d', default=None)
        parents_marriage_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True, get_label="full_location",
                                                 default=Location.query.filter_by(id=Parents.query.get(relationship_id).
                                                                                  marriage_location).scalar())
        ################################################################################################################
        child_forenames = StringField(label="Forenames")
        child_surname = StringField(label="Surname")
        child_gender = SelectField(label='Gender', choices=[choice for choice in genders])
        child_dob = DateField(label='Born', format='%Y-%m-%d', default=None)
        child_birth_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                 get_label="full_location")
        child_dod = DateField(label='Died', format='%Y-%m-%d', default=None)
        child_death_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                 get_label="full_location")

    return FamilyView


def individualview_form(individual_id):
    class IndividualView(FlaskForm):

        individual_forenames = StringField(label="Forenames", default=Individual.query.get(individual_id).forenames)
        individual_surname = StringField(label="Surname", default=Individual.query.get(individual_id).surname)
        individual_gender = SelectField(u'Gender', choices=[choice for choice in genders])
        individual_dob = DateField('Born', format='%Y-%m-%d', default=Individual.query.get(individual_id).dob)
        individual_birth_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                         get_label="full_location", default=Location.query.filter_by
            (id=Individual.query.get(individual_id).birth_location).scalar())
        individual_dod = DateField('Died', format='%Y-%m-%d', default=Individual.query.get(individual_id).dod)
        individual_death_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                         get_label="full_location", default=Location.query.filter_by
            (id=Individual.query.get(individual_id).death_location).scalar())

    return IndividualView


class IndividualView(FlaskForm):

    individual_forenames = StringField(label="Forenames")
    individual_surname = StringField(label="Surname")
    individual_gender = SelectField(u'Gender', choices=[choice for choice in genders])
    individual_dob = DateField('Born', format='%Y-%m-%d')
    individual_birth_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                     get_label="full_location")
    individual_dod = DateField('Died', format='%Y-%m-%d')
    individual_death_location = QuerySelectField("Place", query_factory=location_query, allow_blank=True,
                                                     get_label="full_location")


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
