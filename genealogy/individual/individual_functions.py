from flask import session
from genealogy import db
from genealogy.models import Individual, Parents, FamilyLink, Gender

def fullname(first, last):
    return first + " " + last


def create_partners(type, father_id=None, mother_id=None):
    if db.session.query(Parents).filter_by(father_id=father_id,
                                           mother_id=mother_id).scalar() is None:
        parents = Parents(father_id, mother_id)
        db.session.add(parents)
        db.session.commit()
        db.session.flush()

        if type == "parents":
            session["partners.id"] = parents.id
        elif type == "patgrandparents":
            session["patgrandparents.id"] = parents.id
        elif type == "matgrandparents":
            session["matgrandparents.id"] = parents.id

        return parents.id


def update_partners(type, partners_id, father_id=None, mother_id=None):
    # If there is no father in the partner record, add the father to it:
    if db.session.query(Parents).filter_by(id=partners_id, father_id=father_id).scalar() is None:
        updated_father = db.session.query(Parents).get(partners_id)

        updated_father.father_id = father_id
        db.session.commit()
        db.session.flush()

        if type == "parents":
            session["partners.id"] = updated_father.id
        elif type == "patgrandparents":
            session["patgrandparents.id"] = updated_father.id
        elif type == "matgrandparents":
            session["matgrandparents.id"] = updated_father.id

        return updated_father.id

    # Else if there is no mother in the partner record, add the mother to it:
    elif db.session.query(Parents).filter_by(id=partners_id, mother_id=mother_id).scalar() is None:
        updated_mother = db.session.query(Parents).get(partners_id)
        # parentsid = session["partners.id"]
        updated_mother.mother_id = mother_id
        db.session.commit()
        db.session.flush()

        if type == "parents":
            session["partners.id"] = updated_mother.id
        elif type == "patgrandparents":
            session["patgrandparents.id"] = updated_mother.id
        elif type == "matgrandparents":
            session["matgrandparents.id"] = updated_mother.id

        return updated_mother.id


def link_child(individual_id, parents_id):
    if db.session.query(FamilyLink).filter_by(individual_id=individual_id,
                                              parents_id=parents_id).scalar() is None:
        c = FamilyLink(individual_id, parents_id)
        db.session.add(c)
        db.session.commit()
        db.session.flush()


def add_father(form):
    father_forenames = form.father_forenames.data
    father_surname = form.father_surname.data
    father_gender = Gender.male
    father_dob = form.father_dob.data
    father_fullname = fullname(father_forenames, father_surname)

    new_father = Individual(father_surname, father_fullname, father_forenames, father_gender, father_dob)
    db.session.add(new_father)

    db.session.commit()
    db.session.flush()

    session["father.id"] = new_father.id
    session["father_fullname"] = father_fullname

    if session.get("mother.id") is None:
        create_partners(type="parents", father_id=session["father.id"], mother_id=None)
    else:
        update_partners(type="parents", partners_id=session["partners.id"], father_id=session["father.id"],
                        mother_id=session["mother.id"])

    return


def add_mother(form):
    mother_forenames = form.mother_forenames.data
    mother_surname = form.mother_surname.data
    mother_gender = Gender.female
    mother_dob = form.mother_dob.data
    mother_fullname = fullname(mother_forenames, mother_surname)

    new_mother = Individual(mother_surname, mother_fullname, mother_forenames, mother_gender, mother_dob)
    db.session.add(new_mother)

    db.session.commit()
    db.session.flush()
    session["mother.id"] = new_mother.id

    if session.get("father.id") is None:
        create_partners(type="parents", father_id=None, mother_id=session["mother.id"])
    else:
        update_partners(type="parents", partners_id=session["partners.id"], father_id=session["father.id"],
                        mother_id=session["mother.id"])

    return


def add_patGrandfather(form):
    pat_grandfather_forenames = form.patgrandfather_forenames.data
    pat_grandfather_surname = form.patgrandfather_surname.data
    pat_grandfather_gender = Gender.male
    pat_grandfather_dob = form.patgrandfather_dob.data
    patGrandfather_fullname = fullname(pat_grandfather_forenames, pat_grandfather_surname)

    new_patgrandfather = Individual(pat_grandfather_surname, patGrandfather_fullname, pat_grandfather_forenames,
                                    pat_grandfather_gender, pat_grandfather_dob)
    db.session.add(new_patgrandfather)

    db.session.commit()
    db.session.flush()

    session["patGrandfather.id"] = new_patgrandfather.id

    if session.get("patGrandmother.id") is None:
        create_partners(type="patgrandparents", father_id=session["patGrandfather.id"], mother_id=None)
    else:
        update_partners(type="patgrandparents", partners_id=session["patgrandparents.id"],
                        father_id=session["patGrandfather.id"],
                        mother_id=session["patGrandmother.id"])

    link_child(individual_id=session["father.id"], parents_id=session["patgrandparents.id"])

    return


def add_patGrandmother(form):
    patgrandmother_forenames = form.patgrandmother_forenames.data
    patgrandmother_surname = form.patgrandmother_surname.data
    patgrandmother_gender = Gender.female
    patgrandmother_dob = form.patgrandmother_dob.data
    patgrandmother_fullname = fullname(patgrandmother_forenames, patgrandmother_surname)

    new_patgrandmother = Individual(patgrandmother_surname, patgrandmother_fullname, patgrandmother_forenames,
                                    patgrandmother_gender, patgrandmother_dob)
    db.session.add(new_patgrandmother)

    db.session.commit()
    db.session.flush()

    session["patGrandmother.id"] = new_patgrandmother.id
    session["patGrandmother_fullname"] = patgrandmother_fullname

    if session.get("patGrandfather.id") is None:
        create_partners(type="patgrandparents", father_id=None, mother_id=session["patGrandmother.id"])
    else:
        update_partners(type="patgrandparents", partners_id=session["patgrandparents.id"],
                        father_id=session["patGrandfather.id"],
                        mother_id=session["patGrandmother.id"])

    link_child(individual_id=session["father.id"], parents_id=session["patgrandparents.id"])

    return


def add_matGrandfather(form):
    mat_grandfather_forenames = form.matgrandfather_forenames.data
    mat_grandfather_surname = form.matgrandfather_surname.data
    mat_grandfather_gender = Gender.male
    mat_grandfather_dob = form.matgrandfather_dob.data
    matgrandfather_fullname = fullname(mat_grandfather_forenames, mat_grandfather_surname)

    new_matgrandfather = Individual(mat_grandfather_surname, matgrandfather_fullname, mat_grandfather_forenames,
                                    mat_grandfather_gender, mat_grandfather_dob)
    db.session.add(new_matgrandfather)

    db.session.commit()
    db.session.flush()

    session["matGrandfather.id"] = new_matgrandfather.id

    if session.get("matGrandmother.id") is None:
        create_partners(type="matgrandparents", father_id=session["matGrandfather.id"], mother_id=None)
    else:
        update_partners(type="matgrandparents", partners_id=session["matgrandparents.id"],
                        father_id=session["matGrandfather.id"],
                        mother_id=session["matGrandmother.id"])

    link_child(individual_id=session["mother.id"], parents_id=session["matgrandparents.id"])

    return


def add_matGrandmother(form):
    matgrandmother_forenames = form.matgrandmother_forenames.data
    matgrandmother_surname = form.matgrandmother_surname.data
    matgrandmother_gender = Gender.female
    matgrandmother_dob = form.matgrandmother_dob.data
    matgrandmother_fullname = fullname(matgrandmother_forenames, matgrandmother_surname)

    new_matgrandmother = Individual(matgrandmother_surname, matgrandmother_fullname, matgrandmother_forenames,
                                    matgrandmother_gender, matgrandmother_dob)
    db.session.add(new_matgrandmother)

    db.session.commit()
    db.session.flush()

    session["matGrandmother.id"] = new_matgrandmother.id
    session["matGrandmother_fullname"] = matgrandmother_fullname

    if session.get("matGrandfather.id") is None:
        create_partners(type="matgrandparents", father_id=None, mother_id=session["matGrandmother.id"])
    else:
        update_partners(type="matgrandparents", partners_id=session["matgrandparents.id"],
                        father_id=session["matGrandfather.id"],
                        mother_id=session["matGrandmother.id"])

    link_child(individual_id=session["mother.id"], parents_id=session["matgrandparents.id"])

    return