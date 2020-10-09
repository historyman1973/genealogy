from genealogy import db

family_link = db.Table("family_link",
    db.Column("individual_id", db.Integer, db.ForeignKey("individual.id"), primary_key=True),
    db.Column("parents_id", db.Integer, db.ForeignKey("parents.id"), primary_key=True))


class Individual(db.Model):

    __tablename__ = "individual"

    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.Text)
    middle_name = db.Column(db.Text)
    surname = db.Column(db.Text)

    parents = db.relationship("Parents", secondary="family_link")


    def __init__(self,surname,forename=None,middle_name=None):
        self.forename = forename
        self.middle_name = middle_name
        self.surname = surname

    def __repr__(self):
        pass



class Parents(db.Model):

    __tablename__ = "parents"

    id = db.Column(db.Integer, primary_key=True)
    father_id = db.Column(db.Integer, db.ForeignKey("individual.id"))
    mother_id = db.Column(db.Integer, db.ForeignKey("individual.id"))

    children = db.relationship("Individual", secondary="family_link")

    def __init__(self, father_id=None,mother_id=None):
        self.father_id = father_id
        self.mother_id = mother_id


db.create_all()
