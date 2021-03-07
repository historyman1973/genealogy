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

    def __init__(self, **kwargs):
        super(Individual, self).__init__(**kwargs)


class Parents(db.Model):
    __tablename__ = "parents"

    id = db.Column(db.Integer, primary_key=True)
    father_id = db.Column(db.Integer, db.ForeignKey("individual.id"))
    mother_id = db.Column(db.Integer, db.ForeignKey("individual.id"))
    dom = db.Column(db.Date)

    children = db.relationship("Individual", secondary=FamilyLink.__table__)

    def __init__(self, **kwargs):
        super(Parents, self).__init__(**kwargs)



db.create_all()
