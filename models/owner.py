from db import db


class OwnerModel(db.Model):
    __tablename__ = "owners"

    id = db.Column(db.Integer, primary_key=True)
    identity = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    cars = db.relationship('AssociationModel', back_populates='owner', lazy='dynamic')


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_identity(cls, identity):
        return cls.query.filter_by(identity=identity).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()