from flask import session
from genealogy import db
from genealogy.models import Individual, Parents, FamilyLink
from dateutil import relativedelta
from datetime import datetime


def add_person(form, role):
    individual_forenames = form.individual_forenames.data
    individual_surname = form.individual_surname.data
    # Override gender if the role in the family is known
    if role == "patgrandfather" or role == "matgrandfather" or role == "father" or role == "motherspartner":
        form.individual_gender.data = "Male"
    elif role == "matgrandfather" or role == "matgrandmother" or role == "mother" or role == "fatherspartner":
        form.individual_gender.data = "Female"
    individual_gender = form.individual_gender.data
    individual_dob = form.individual_dob.data
    if form.individual_birth_location.data:
        individual_birth_location = form.individual_birth_location.data.id
    else:
        individual_birth_location = form.individual_birth_location.data
    individual_dod = form.individual_dod.data
    if form.individual_death_location.data:
        individual_death_location = form.individual_death_location.data.id
    else:
        individual_death_location = form.individual_death_location.data

    individual_age = calculate_period(individual_dob, individual_dod)
    individual_fullname = fullname(individual_forenames, individual_surname)

    new_individual = Individual(surname=individual_surname, fullname=individual_fullname, forenames=individual_forenames,
                           gender=individual_gender, dob=individual_dob, dod=individual_dod, age=individual_age,
                           birth_location=individual_birth_location, death_location=individual_death_location)
    db.session.add(new_individual)

    db.session.commit()
    db.session.flush()

    session["new_individual_id"] = new_individual.id

    return


def add_child():

    session["child.id"] = session["new_individual_id"]

    link_child(individual_id=session["child.id"], parents_id=session["partners.id"])

    # Handles male and female children only
    create_child_partnership(Individual.query.get_or_404(session["new_individual_id"]))

    session.pop("new_individual_id", None)

    return


def add_father():

    session["father.id"] = session["new_individual_id"]
    session.pop("new_individual_id", None)

    if session.get("mother.id") is None:
        create_partners(partner_type="parents", father_id=session["father.id"], mother_id=None)
    else:
        update_partners(partner_type="parents", partners_id=session["partners.id"], father_id=session["father.id"],
                        mother_id=session["mother.id"])

    return


def add_mother():

    session["mother.id"] = session["new_individual_id"]
    session.pop("new_individual_id", None)

    if session.get("father.id") is None:
        create_partners(partner_type="parents", father_id=None, mother_id=session["mother.id"])
    else:
        update_partners(partner_type="parents", partners_id=session["partners.id"], father_id=session["father.id"],
                        mother_id=session["mother.id"])

    return


def add_matgrandfather():

    session["matgrandfather.id"] = session["new_individual_id"]
    session.pop("new_individual_id", None)

    if session.get("matgrandmother.id") is None:
        create_partners(partner_type="matgrandparents", father_id=session["matgrandfather.id"], mother_id=None)
    else:
        update_partners(partner_type="matgrandparents", partners_id=session["matgrandparents.id"],
                        father_id=session["matgrandfather.id"],
                        mother_id=session["matgrandmother.id"])

    link_child(individual_id=session["mother.id"], parents_id=session["matgrandparents.id"])

    return


def add_matgrandmother():

    session["matgrandmother.id"] = session["new_individual_id"]
    session.pop("new_individual_id", None)

    if session.get("matgrandfather.id") is None:
        create_partners(partner_type="matgrandparents", father_id=None, mother_id=session["matgrandmother.id"])
    else:
        update_partners(partner_type="matgrandparents", partners_id=session["matgrandparents.id"],
                        father_id=session["matgrandfather.id"],
                        mother_id=session["matgrandmother.id"])

    link_child(individual_id=session["mother.id"], parents_id=session["matgrandparents.id"])

    return


def add_partner(forwhom):

    if forwhom == "father":
        session["mother.id"] = session["new_individual_id"]
    elif forwhom == "mother":
        session["father.id"] = session["new_individual_id"]
    session.pop("new_individual_id", None)

    create_partners(partner_type="parents", father_id=session["father.id"], mother_id=session["mother.id"])

    return


def add_patgrandfather():

    session["patgrandfather.id"] = session["new_individual_id"]
    session.pop("new_individual_id", None)

    if session.get("patgrandmother.id") is None:
        create_partners(partner_type="patgrandparents", father_id=session["patgrandfather.id"], mother_id=None)
    else:
        update_partners(partner_type="patgrandparents", partners_id=session["patgrandparents.id"],
                        father_id=session["patgrandfather.id"],
                        mother_id=session["patgrandmother.id"])

    link_child(individual_id=session["father.id"], parents_id=session["patgrandparents.id"])

    return


def add_patgrandmother():

    session["patgrandmother.id"] = session["new_individual_id"]
    session.pop("new_individual_id", None)

    if session.get("patgrandfather.id") is None:
        create_partners(partner_type="patgrandparents", father_id=None, mother_id=session["patgrandmother.id"])
    else:
        update_partners(partner_type="patgrandparents", partners_id=session["patgrandparents.id"],
                        father_id=session["patgrandfather.id"],
                        mother_id=session["patgrandmother.id"])

    link_child(individual_id=session["father.id"], parents_id=session["patgrandparents.id"])

    return


def calculate_period(born, died):
    # If there are known birth and death dates, calculate the age
    if born and died:

        age = relativedelta.relativedelta(died, born)

        return int(age.years)

    # If the person was born over 100 years ago, don't calculate the age
    elif relativedelta.relativedelta(datetime.today(), born).years > 100:
        return None

    # If the person has no birth or death dates, don't calculate the age
    elif born is None and died is None:
        return None

    # If there is just no birth date, don't calculate the age
    elif born is None:
        return None

    # If the person was born less than 100 years ago and there's no death date, calculate current age
    elif relativedelta.relativedelta(datetime.today(), born).years < 100 and died is None:

        age = relativedelta.relativedelta(datetime.today(), born)

        return int(age.years)


def create_child_partnership(new_child):
    if new_child.gender == "Male":
        create_partners(partner_type="child", father_id=new_child.id, mother_id=None)
    elif new_child.gender == "Female":
        create_partners(partner_type="child", father_id=None, mother_id=new_child.id)


def create_partners(partner_type, father_id=None, mother_id=None):
    if db.session.query(Parents).filter_by(father_id=father_id,
                                           mother_id=mother_id).scalar() is None:
        parents = Parents(father_id=father_id, mother_id=mother_id)
        db.session.add(parents)
        db.session.commit()
        db.session.flush()

        if partner_type == "parents":
            session["partners.id"] = parents.id
        elif partner_type == "patgrandparents":
            session["patgrandparents.id"] = parents.id
        elif partner_type == "matgrandparents":
            session["matgrandparents.id"] = parents.id
        elif partner_type == "child":
            pass

        return parents.id


def delete_individual(id):
    familylinks = FamilyLink.query.filter(FamilyLink.individual_id == id)

    # Delete all FamilyLink records where individual is a child of existing parents
    for familylink in familylinks:
        db.session.delete(familylink)

    # Find all parent records for the individual.  If partner present, remove the deleted individual from the record
    # but if there will be no-one left in the parent record once the individual is deleted, remove the whole record
    if Individual.query.get_or_404(id).gender == "Male":
        parentrecords = Parents.query.filter(Parents.father_id == id)

        for parentrecord in parentrecords:
            if parentrecord.mother_id is not None:
                parentrecord.father_id = None
                db.session.commit()
            else:
                db.session.delete(parentrecord)
                db.session.commit()

    elif Individual.query.get_or_404(id).gender == "Female":
        parentrecords = Parents.query.filter(Parents.mother_id == id)

        for parentrecord in parentrecords:
            if parentrecord.father_id is not None:
                parentrecord.mother_id = None
                db.session.commit()
            else:
                db.session.delete(parentrecord)
                db.session.commit()

    # Remove the individual's session data if they're the current grandparent or parent
    if session.get("patgrandfather.id") is not None:
        if id == session["patgrandfather.id"]:
            session.pop("patgrandfather.id", None)
    elif session.get("patgrandmother.id") is not None:
        if id == session["patgrandmother.id"]:
            print("Removing individual: " + str(session["patgrandmother.id"]))
            session.pop("patgrandmother.id", None)
    elif session.get("matgrandfather.id") is not None:
        if id == session["matgrandfather.id"]:
            print("Removing individual: " + str(session["matgrandfather.id"]))
            session.pop("matgrandfather.id", None)
    elif session.get("matgrandmother.id") is not None:
        if id == session["matgrandmother.id"]:
            print("Removing individual: " + str(session["matgrandmother.id"]))
            session.pop("matgrandmother.id", None)
    elif id == session["father.id"]:
        session.pop("father.id", None)
    elif id == session["mother.id"]:
        session.pop("mother.id", None)

    # When all of the other links are removed, delete the individual
    db.session.delete(Individual.query.get_or_404(id))
    db.session.commit()


def fullname(first, last):
    return first + " " + last


def link_child(individual_id, parents_id):
    if db.session.query(FamilyLink).filter_by(individual_id=individual_id,
                                              parents_id=parents_id).scalar() is None:
        c = FamilyLink(individual_id, parents_id)
        db.session.add(c)
        db.session.commit()
        db.session.flush()


def query_children(parentsid):
    children = db.session.query(Individual) \
        .join(FamilyLink) \
        .filter(FamilyLink.parents_id == parentsid) \
        .filter(FamilyLink.individual_id == Individual.id).order_by(Individual.dob)
    return children


def session_pop_grandparents():
    session.pop("patgrandfather.id", None)
    session.pop("patgrandmother.id", None)
    session.pop("matgrandfather.id", None)
    session.pop("matgrandmother.id", None)


def update_partners(partner_type, partners_id, father_id=None, mother_id=None):
    # If there is no father in the partner record, add the father to it:
    if db.session.query(Parents).filter_by(id=partners_id, father_id=father_id).scalar() is None:
        updated_father = db.session.query(Parents).get_or_404(partners_id)

        updated_father.father_id = father_id
        db.session.commit()
        db.session.flush()

        if partner_type == "parents":
            session["partners.id"] = updated_father.id
        elif partner_type == "patgrandparents":
            session["patgrandparents.id"] = updated_father.id
        elif partner_type == "matgrandparents":
            session["matgrandparents.id"] = updated_father.id

        return updated_father.id

    # Else if there is no mother in the partner record, add the mother to it:
    elif db.session.query(Parents).filter_by(id=partners_id, mother_id=mother_id).scalar() is None:
        updated_mother = db.session.query(Parents).get_or_404(partners_id)
        # parentsid = session["partners.id"]
        updated_mother.mother_id = mother_id
        db.session.commit()
        db.session.flush()

        if partner_type == "parents":
            session["partners.id"] = updated_mother.id
        elif partner_type == "patgrandparents":
            session["patgrandparents.id"] = updated_mother.id
        elif partner_type == "matgrandparents":
            session["matgrandparents.id"] = updated_mother.id

        return updated_mother.id
