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
    birth_location = db.Column(db.Integer, db.ForeignKey("location.id"))
    birth_location_rel = db.relationship("Location", foreign_keys="[Individual.birth_location]")
    dod = db.Column(db.Date)
    death_location = db.Column(db.Integer, db.ForeignKey("location.id"))
    death_location_rel = db.relationship("Location", foreign_keys="[Individual.death_location]")
    age = db.Column(db.Integer)

    parents = db.relationship("Parents", secondary=FamilyLink.__table__)

    def __init__(self, **kwargs):
        super(Individual, self).__init__(**kwargs)


class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text)
    parish = db.Column(db.Text)
    district = db.Column(db.Text)
    townorcity = db.Column(db.Text)
    county = db.Column(db.Text)
    country = db.Column(db.Text)
    short_location = db.Column(db.Text)
    full_location = db.Column(db.Text)

    def __init__(self, **kwargs):
        super(Location, self).__init__(**kwargs)

    def __repr__(self):
        return self.full_location


class Parents(db.Model):
    __tablename__ = "parents"

    id = db.Column(db.Integer, primary_key=True)
    father_id = db.Column(db.Integer, db.ForeignKey("individual.id"))
    father_fullname_rel = db.relationship("Individual", foreign_keys="[Parents.father_id]")
    mother_id = db.Column(db.Integer, db.ForeignKey("individual.id"))
    mother_fullname_rel = db.relationship("Individual", foreign_keys="[Parents.mother_id]")
    dom = db.Column(db.Date)
    marriage_location = db.Column(db.Integer, db.ForeignKey("location.id"))

    children = db.relationship("Individual", secondary=FamilyLink.__table__)

    def __init__(self, **kwargs):
        super(Parents, self).__init__(**kwargs)


db.create_all()
