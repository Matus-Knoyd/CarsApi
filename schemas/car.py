from ma import ma
from db import db
from models.car import CarModel 
from models.owner import OwnerModel # musi byt
from models.association import AssociationModel # musi byt

class CarSchema(ma.SQLAlchemyAutoSchema):
    owners = ma.Nested("schemas.association.AssociationSchema", exclude=("car", 'car_id'), many=True)
    
    class Meta:
        model = CarModel
        load_instance = True
        dump_only = ('id',)
        include_fk = True
        sqla_session = db.session
