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

from models.car import CarModel
from schemas.car import CarSchema
from strings.messages import get_message

car_schema = CarSchema()
cars_schema_not_logged = CarSchema(only=('vin',))
cars_schema_logged = CarSchema(exclude=('owners',))

class Car(Resource):
    @classmethod
    @jwt_required
    def get(cls,id_):
        car = CarModel.find_by_id(id_)
        if not car:
            return {"message": get_message('car_not_found')}, 404 # NOT FOUND
        return car_schema.dump(car), 200 # OK

    @classmethod
    @jwt_required
    def delete(cls,id_):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": get_message('admin_required')}, 401 # UNAUTHORIZED

        car = CarModel.find_by_id(id_)
        if not car:
            return {"message": get_message('user_not_found')}, 404 # NOT FOUND
        
        car.delete_from_db()
        return {"message": get_message('car_deleted')}, 200 # OK


class CarRegister(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        car = car_schema.load(request.get_json())

        if CarModel.find_by_vin(car.vin):
            return {"message": get_message('car_vin_exists')}, 400 # BAD REQUEST
        
        car.save_to_db()

        return {"message": get_message('car_created')}, 201 # CREATED


class Cars(Resource):
    @classmethod
    @jwt_optional
    def get(cls):
        identity = get_jwt_identity()
        cars = CarModel.find_all()
        
        if identity:
            return {'cars': cars_schema_logged.dump(cars, many=True)}, 200
        
        return {'cars': cars_schema_not_logged.dump(cars, many=True),
                'message' : get_message('login_for_details')}, 200


