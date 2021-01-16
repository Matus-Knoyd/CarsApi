from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, nullable =False, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def json(self, with_password=False):
        all_attributes = {k:v for k,v in self.__dict__.items() if not k.startswith('_')}
        
        if not with_password:
            del all_attributes['password']
        
        return all_attributes

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()