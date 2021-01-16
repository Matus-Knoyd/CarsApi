from flask_restful import Resource, reqparse
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    fresh_jwt_required, 
    get_jwt_claims,
    jwt_required,
    jwt_optional,
    get_jwt_identity
)    

from models.association import AssociationModel
from models.car import CarModel
from models.owner import OwnerModel

from schemas.association import AssociationSchema
from schemas.car import CarSchema
from schemas.owner import OwnerSchema

from strings.messages import get_message

assiciation_schema = AssociationSchema()
car_schema = CarSchema(exclude=('owners',))
owner_schema = OwnerSchema(exclude=('cars',))

class OwnersFinder(Resource):
    @classmethod
    @jwt_required
    def get(cls,id_):
        associations = AssociationModel.find_by_car_id(id_)
        if not associations:
            return {"message": get_message('owners_not_found')}, 404 # NOT FOUND
        return {'owners': [owner_schema.dump(a.owner) for a in associations]}, 200 # OK


class CarsFinder(Resource):
    @classmethod
    @jwt_required
    def get(cls,id_):
        associations = AssociationModel.find_by_owner_id(id_)
        if not associations:
            return {"message": get_message('cars_not_found')}, 404 # NOT FOUND
        return {'cars': [car_schema.dump(a.car) for a in associations]}, 200 # OK


class AssociationAdder(Resource):
    @classmethod
    @jwt_required
    def put(cls):
        association_data = assiciation_schema.load(request.get_json())

        car = CarModel.find_by_id(association_data['car_id'])
        if not car:
            return {"message": get_message('car_not_found')}, 404 # NOT FOUND
        
        owner = OwnerModel.find_by_id(association_data['owner_id'])
        if not owner:
            return {"message": get_message('ownner_not_found')}, 404 # NOT FOUND

        association = AssociationModel.find_by_primary_key(association_data['car_id'], association_data['owner_id'])
        if association:
            association.from_date = association_data['from_date']
            association.to_date = association_data['to_date']
        else:
            association = AssociationModel(**association_data)

        association.save_to_db()
        return {"message": get_message('association_created_updated')}, 201 # CREATED
