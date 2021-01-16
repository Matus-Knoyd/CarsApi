from ma import ma
from db import db
from models.car import CarModel
from models.owner import OwnerModel
from models.association import AssociationModel

class OwnerSchema(ma.SQLAlchemyAutoSchema):
    cars = ma.Nested("schemas.association.AssociationSchema", exclude=('owner','owner_id'), many=True)
    
    class Meta:
        model = OwnerModel
        load_instance = True
        dump_only = ('id',)
        include_fk = True
        sqla_session = db.session

    