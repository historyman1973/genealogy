from flask import session
from genealogy import db
from genealogy.models import Individual, Parents, FamilyLink
from dateutil import relativedelta
from datetime import datetime


def add_child(form):
    child_forenames = form.individual_forenames.data
    child_surname = form.individual_surname.data
    child_gender = form.individual_gender.data
    child_dob = form.individual_dob.data
    if form.individual_birth_location.data:
        child_birth_location = form.individual_birth_location.data.id
    else:
        child_birth_location = form.individual_birth_location.data
    child_dod = form.individual_dod.data
    if form.individual_death_location.data:
        child_death_location = form.individual_death_location.data.id
    else:
        child_death_location = form.individual_death_location.data

    child_age = calculate_period(child_dob, child_dod)
    child_fullname = fullname(child_forenames, child_surname)

    new_child = Individual(surname=child_surname, fullname=child_fullname, forenames=child_forenames,
                           gender=child_gender, dob=child_dob, dod=child_dod, age=child_age,
                           birth_location=child_birth_location, death_location=child_death_location)
    db.session.add(new_child)

    db.session.commit()
    db.session.flush()

    session["child.id"] = new_child.id

    link_child(individual_id=session["child.id"], parents_id=session["partners.id"])

    # Handles male and female children only
    create_child_partnership(new_child)

    # children = db.session.query(Individual) \
    #     .join(FamilyLink) \
    #     .filter(FamilyLink.parents_id == session["partners.id"]) \
    #     .filter(FamilyLink.individual_id == Individual.id).order_by(Individual.dob)
    #
    # number_children = children.count()

    return


def add_father(form):
    father_forenames = form.individual_forenames.data
    father_surname = form.individual_surname.data
    father_gender = "Male"
    father_dob = form.individual_dob.data
    if form.individual_birth_location.data:
        father_birth_location = form.individual_birth_location.data.id
    else:
        father_birth_location = form.individual_birth_location.data
    father_dod = form.individual_dod.data
    if form.individual_death_location.data:
        father_death_location = form.individual_death_location.data.id
    else:
        father_death_location = form.individual_death_location.data
    father_fullname = fullname(father_forenames, father_surname)
    father_age = calculate_period(father_dob, father_dod)

    new_father = Individual(surname=father_surname, fullname=father_fullname, forenames=father_forenames,
                            gender=father_gender, dob=father_dob, birth_location=father_birth_location,
                            dod=father_dod, death_location=father_death_location,
                            age=father_age)
    db.session.add(new_father)

    db.session.commit()
    db.session.flush()

    session["father.id"] = new_father.id
    session["father_fullname"] = father_fullname

    if session.get("mother.id") is None:
        create_partners(partner_type="parents", father_id=session["father.id"], mother_id=None)
    else:
        update_partners(partner_type="parents", partners_id=session["partners.id"], father_id=session["father.id"],
                        mother_id=session["mother.id"])

    return


def add_mother(form):
    mother_forenames = form.individual_forenames.data
    mother_surname = form.individual_surname.data
    mother_gender = "Female"
    mother_dob = form.individual_dob.data
    if form.individual_birth_location.data:
        mother_birth_location = form.individual_birth_location.data.id
    else:
        mother_birth_location = form.individual_birth_location.data
    mother_dod = form.individual_dod.data
    if form.individual_death_location.data:
        mother_death_location = form.individual_death_location.data.id
    else:
        mother_death_location = form.individual_death_location.data
    mother_fullname = fullname(mother_forenames, mother_surname)
    mother_age = calculate_period(mother_dob, mother_dod)

    new_mother = Individual(surname=mother_surname, fullname=mother_fullname, forenames=mother_forenames,
                            gender=mother_gender, dob=mother_dob, birth_location=mother_birth_location,
                            dod=mother_dod, death_location=mother_death_location,
                            age=mother_age)
    db.session.add(new_mother)

    db.session.commit()
    db.session.flush()
    session["mother.id"] = new_mother.id

    if session.get("father.id") is None:
        create_partners(partner_type="parents", father_id=None, mother_id=session["mother.id"])
    else:
        update_partners(partner_type="parents", partners_id=session["partners.id"], father_id=session["father.id"],
                        mother_id=session["mother.id"])

    return


def add_matgrandfather(form):
    matgrandfather_forenames = form.individual_forenames.data
    matgrandfather_surname = form.individual_surname.data
    matgrandfather_gender = "Male"
    matgrandfather_dob = form.individual_dob.data
    if form.individual_birth_location.data:
        matgrandfather_birth_location = form.individual_birth_location.data.id
    else:
        matgrandfather_birth_location = form.individual_birth_location.data
    matgrandfather_dod = form.individual_dod.data
    if form.individual_death_location.data:
        matgrandfather_death_location = form.individual_death_location.data.id
    else:
        matgrandfather_death_location = form.individual_death_location.data
    matgrandfather_fullname = fullname(matgrandfather_forenames, matgrandfather_surname)
    mat_grandfather_age = calculate_period(matgrandfather_dob, matgrandfather_dod)

    new_matgrandfather = Individual(surname=matgrandfather_surname, fullname=matgrandfather_fullname,
                                    forenames=matgrandfather_forenames, gender=matgrandfather_gender,
                                    dob=matgrandfather_dob, birth_location=matgrandfather_birth_location,
                                    dod=matgrandfather_dod, death_location=matgrandfather_death_location,
                                    age=mat_grandfather_age)
    db.session.add(new_matgrandfather)

    db.session.commit()
    db.session.flush()

    session["matgrandfather.id"] = new_matgrandfather.id

    if session.get("matgrandmother.id") is None:
        create_partners(partner_type="matgrandparents", father_id=session["matgrandfather.id"], mother_id=None)
    else:
        update_partners(partner_type="matgrandparents", partners_id=session["matgrandparents.id"],
                        father_id=session["matgrandfather.id"],
                        mother_id=session["matgrandmother.id"])

    link_child(individual_id=session["mother.id"], parents_id=session["matgrandparents.id"])

    return


def add_matgrandmother(form):
    matgrandmother_forenames = form.individual_forenames.data
    matgrandmother_surname = form.individual_surname.data
    matgrandmother_gender = "Female"
    matgrandmother_dob = form.individual_dob.data
    if form.individual_birth_location.data:
        matgrandmother_birth_location = form.individual_birth_location.data.id
    else:
        matgrandmother_birth_location = form.individual_birth_location.data
    matgrandmother_dod = form.individual_dod.data
    if form.individual_death_location.data:
        matgrandmother_death_location = form.individual_death_location.data.id
    else:
        matgrandmother_death_location = form.individual_death_location.data
    matgrandmother_fullname = fullname(matgrandmother_forenames, matgrandmother_surname)
    matgrandmother_age = calculate_period(matgrandmother_dob, matgrandmother_dod)

    new_matgrandmother = Individual(surname=matgrandmother_surname, fullname=matgrandmother_fullname,
                                    forenames=matgrandmother_forenames, gender=matgrandmother_gender,
                                    dob=matgrandmother_dob, birth_location=matgrandmother_birth_location,
                                    dod=matgrandmother_dod, death_location=matgrandmother_death_location,
                                    age=matgrandmother_age)
    db.session.add(new_matgrandmother)

    db.session.commit()
    db.session.flush()

    session["matgrandmother.id"] = new_matgrandmother.id
    session["matgrandmother_fullname"] = matgrandmother_fullname

    if session.get("matgrandfather.id") is None:
        create_partners(partner_type="matgrandparents", father_id=None, mother_id=session["matgrandmother.id"])
    else:
        update_partners(partner_type="matgrandparents", partners_id=session["matgrandparents.id"],
                        father_id=session["matgrandfather.id"],
                        mother_id=session["matgrandmother.id"])

    link_child(individual_id=session["mother.id"], parents_id=session["matgrandparents.id"])

    return


def add_patgrandfather(form):

    patgrandfather_forenames = form.individual_forenames.data
    patgrandfather_surname = form.individual_surname.data
    patgrandfather_gender = "Male"
    patgrandfather_dob = form.individual_dob.data
    if form.individual_birth_location.data:
        patgrandfather_birth_location = form.individual_birth_location.data.id
    else:
        patgrandfather_birth_location = form.individual_birth_location.data
    patgrandfather_dod = form.individual_dod.data
    if form.individual_death_location.data:
        patgrandfather_death_location = form.individual_death_location.data.id
    else:
        patgrandfather_death_location = form.individual_death_location.data
    patgrandfather_fullname = fullname(patgrandfather_forenames, patgrandfather_surname)
    patgrandfather_age = calculate_period(patgrandfather_dob, patgrandfather_dod)

    new_patgrandfather = Individual(surname=patgrandfather_surname, fullname=patgrandfather_fullname,
                                    forenames=patgrandfather_forenames, gender=patgrandfather_gender,
                                    dob=patgrandfather_dob, dod=patgrandfather_dod, age=patgrandfather_age,
                                    birth_location=patgrandfather_birth_location,
                                    death_location=patgrandfather_death_location)
    db.session.add(new_patgrandfather)

    db.session.commit()
    db.session.flush()

    session["patgrandfather.id"] = new_patgrandfather.id

    if session.get("patgrandmother.id") is None:
        create_partners(partner_type="patgrandparents", father_id=session["patgrandfather.id"], mother_id=None)
    else:
        update_partners(partner_type="patgrandparents", partners_id=session["patgrandparents.id"],
                        father_id=session["patgrandfather.id"],
                        mother_id=session["patgrandmother.id"])

    link_child(individual_id=session["father.id"], parents_id=session["patgrandparents.id"])

    return


def add_patgrandmother(form):
    patgrandmother_forenames = form.individual_forenames.data
    patgrandmother_surname = form.individual_surname.data
    patgrandmother_gender = "Female"
    patgrandmother_dob = form.individual_dob.data
    if form.individual_birth_location.data:
        patgrandmother_birth_location = form.individual_birth_location.data.id
    else:
        patgrandmother_birth_location = form.individual_birth_location.data
    patgrandmother_dod = form.individual_dod.data
    patgrandmother_death_location = form.individual_death_location.data.id
    patgrandmother_fullname = fullname(patgrandmother_forenames, patgrandmother_surname)
    pat_grandmother_age = calculate_period(patgrandmother_dob, patgrandmother_dod)

    new_patgrandmother = Individual(surname=patgrandmother_surname, fullname=patgrandmother_fullname,
                                    forenames=patgrandmother_forenames, gender=patgrandmother_gender,
                                    dob=patgrandmother_dob, birth_location=patgrandmother_birth_location,
                                    dod=patgrandmother_dod, death_location=patgrandmother_death_location,
                                    age=pat_grandmother_age)
    db.session.add(new_patgrandmother)

    db.session.commit()
    db.session.flush()

    session["patgrandmother.id"] = new_patgrandmother.id
    session["patgrandmother_fullname"] = patgrandmother_fullname

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
