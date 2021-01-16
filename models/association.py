from db import db

class AssociationModel(db.Model):
    __tablename__ = "associations"

    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), primary_key=True)
    from_date = db.Column(db.String(256), nullable=False)
    to_date = db.Column(db.String(256),nullable=False)
    car = db.relationship("CarModel", back_populates='owners')
    owner = db.relationship("OwnerModel", back_populates='cars')
        
    @classmethod
    def find_by_car_id(cls, _id):
        return cls.query.filter_by(car_id=_id).all()
    
    @classmethod
    def find_by_owner_id(cls, _id):
        return cls.query.filter_by(owner_id=_id).all()
    
    @classmethod
    def find_by_primary_key(cls, car_id, owner_id):
        return cls.query.filter_by(car_id=car_id, owner_id=owner_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()