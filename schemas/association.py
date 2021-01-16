from ma import ma
from db import db
from models.car import CarModel # musi tu byt pretoze pouzivame car
from models.owner import OwnerModel # musi tu byt pretoze pouzivame owner
from models.association import AssociationModel


class AssociationSchema(ma.SQLAlchemyAutoSchema):
    car = ma.Nested("schemas.car.CarSchema", exclude=("owners",))
    owner = ma.Nested("schemas.owner.OwnerSchema", exclude=("cars",))
    
    class Meta:
        model = AssociationModel
        load_instance = False
        include_fk = True
        sqla_session = db.session