from genealogy import db

genders = ["Male", "Female", "Unknown"]

class FamilyLink(db.Model):
    __tablename__ = "family_link"

    individual_id = db.Column(db.Integer, db.ForeignKey("individual.id"), primary_key=True)
    parents_id = db.Column(db.Integer, db.ForeignKey("parents.id"), primary_key=True)

    def __init__(self, individual_id, parents_id):
        self.individual_id = individual_id
        self.parents_id = parents_id


class Individual(db.Model):
    __tablename__ = "individual"

    id = db.Column(db.Integer, primary_key=True)
    forenames = db.Column(db.Text)
    surname = db.Column(db.Text)
    fullname = db.Column(db.Text)
    gender = db.Column(db.Text)
    dob = db.Column(db.Date)
    dod = db.Column(db.Date)
    age = db.Column(db.Integer)

    parents = db.relationship("Parents", secondary=FamilyLink.__table__)

    def __init__(self, surname, fullname=None, forenames=None, gender="Unknown", dob=None, dod=None, age=None):
        self.forenames = forenames
        self.surname = surname
        self.gender = gender
        self.dob = dob
        self.dod = dod
        self.fullname = fullname
        self.age = age


    # def __repr__(self):
    #     return (str(self.fullname))


class Parents(db.Model):
    __tablename__ = "parents"

    id = db.Column(db.Integer, primary_key=True)
    father_id = db.Column(db.Integer, db.ForeignKey("individual.id"))
    mother_id = db.Column(db.Integer, db.ForeignKey("individual.id"))

    children = db.relationship("Individual", secondary=FamilyLink.__table__)

    def __init__(self, father_id=None, mother_id=None):
        self.father_id = father_id
        self.mother_id = mother_id

    # def __repr__ (self):
    #     return f"Father ID: {self.father_id} Mother ID: {self.mother_id}"


db.create_all()
