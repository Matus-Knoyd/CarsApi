from db import db

class CarModel(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(80), nullable=False)
    brand = db.Column(db.String(80))
    model = db.Column(db.String(80))
    year = db.Column(db.Integer)
    power = db.Column(db.Integer)
    color = db.Column(db.String(80))
    owners = db.relationship("AssociationModel", back_populates='car', lazy='dynamic')
        
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_vin(cls, vin):
        return cls.query.filter_by(vin=vin).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()